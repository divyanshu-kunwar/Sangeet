import os
from dotenv import load_dotenv
from celery.schedules import crontab
from datetime import datetime
import pytz 

load_dotenv("development.env")

def IST_to_UTC(hours, minutes):
    now_in_ist = datetime.now(pytz.timezone("Asia/Kolkata"))
    target_time_in_ist = now_in_ist.replace(hour=hours, minute=minutes, second=0, microsecond=0)
    target_time_in_utc = target_time_in_ist.astimezone(pytz.utc)
    return target_time_in_utc

class Config(object):
    Debug = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    EMAIL = os.getenv('EMAIL')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    SMTP_PORT = os.getenv('SMTP_PORT')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL="redis://127.0.0.1"
    CELERY_CONFIG={"broker_url": "redis://127.0.0.1", 
                     "result_backend": "redis://127.0.0.1", 
    "beat_schedule": {
            "collect_analytics":{
                "task": "utility.tasks.collect_analytics",
                "schedule" : crontab(minute=IST_to_UTC(5, 53).minute, hour = IST_to_UTC(5, 53).hour) 
            },
            "send_notifications" : {
                "task": "utility.tasks.send_notification",
                "schedule": crontab(minute=IST_to_UTC(16, 0).minute, hour = IST_to_UTC(16, 0).hour) 
                # "schedule": 60
            },
            "send_analytics":{
                "task": "utility.tasks.send_analytics",
                "schedule": crontab(0, 0, day_of_month='28')
                # "schedule" : 60
            }
    }
    
    }


# "schedule": crontab( minute="0", hour="*/6")
# "schedule" : 60.0

#         "beat_schedule": {
            # 

            # 
