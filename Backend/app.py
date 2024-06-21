import sys
from flask import Flask , render_template

from utility.model import db
from utility.api import api
from utility.cache import cache
from utility.initial_data import create_initials
from API import *
from utility.celery import make_celery
from config import Config
from flask_cors import CORS

app = Flask(__name__ , 
            static_url_path='', 
            static_folder='static',)
CORS(app)

app.config.from_object(Config)

with app.app_context():
    api.init_app(app)
    db.init_app(app)   
    cache.init_app(app)
    celery = make_celery(app)
    celery.set_default() 
    if(len(sys.argv) > 1 and sys.argv[1]=='-r'):
        create_initials(1)
    else:
        create_initials(0)

    
def get_app_celery():
    return app , celery

def get_cache():
    return cache

@app.route('/')
def index():
    return render_template("index.html")

if(__name__ == "__main__"):
    app.run()