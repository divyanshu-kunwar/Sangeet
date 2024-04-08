from flask import request
from flask_restful import Resource

from controller.c_notification import getNotifications, deleteNotification
from controller.c_user import verify_token
from utility.api import api

class Notification(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            user_id = verify_token(token)['id']
            if(user_id):
                return getNotifications(user_id)
            else:
                return {
                    "success":False,
                    "message": "❌ You are not authorized to use this resource \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }
    
    def delete(self):
        token = request.headers.get('Authorization')
        id = request.args.get('id')
        if(token):
            user_id = verify_token(token)['id']
            if(user_id):
                return deleteNotification(id, user_id)
            else:
                return {
                    "success":False,
                    "message": "❌ You are not authorized to use this resource \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }
    
api.add_resource(Notification, '/api/notifications')