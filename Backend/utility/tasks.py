from celery import shared_task
from controller.c_user import getUserNotVisited
from flask import current_app , render_template
from utility.mailer import Mail
from controller.c_song import getLatestSongs
from controller.c_notification import addNotification
from controller.c_analytics import updateAnalyticsAll
import json

from utility.model import User
from utility.PDFGenerator import generate_report

@shared_task
def send_notification():
    # send notification to all the user who has not visited the site today
    data_users = getUserNotVisited()
    mail = Mail(current_app)
    latest = getLatestSongs(6)
    latest_1 = latest["data"][:3]
    latest_2 = latest["data"][3:6]
    for user in data_users:
        msg_string = render_template('notification.html', user=user , latest_songs=[latest_1, latest_2])
        result = mail.send(subject="Latest Songs From Sangeet", to_email=user["email"], htmlbody=msg_string)
        if(result == True):
            print("Sent Mail to ", user["name"], "\n")
            # save this to database 
            new_string_msg ={
                "Subject" : "You haven't visited us for so long. So we thought of letting you know some of the latest songs that we have added to our ever growing library.",
                "html":  render_template('notification2.html', latest_songs=[latest_1, latest_2])
            }
            new_string_msg = json.dumps(new_string_msg)
            addNotification(user["id"] , new_string_msg)
        else:
            print("Could Not Sent Mail to ",user["name"] , "\n")
    print("Done sent all notifications \n\n")

@shared_task
def collect_analytics():
    print("Started Adding Current Analytics to Database")
    updateAnalyticsAll()

@shared_task
def send_analytics():
    data_users = User.query.all()
    for user in data_users:
        if(user.role == 3):
            generate_report(user.id , user.email)

