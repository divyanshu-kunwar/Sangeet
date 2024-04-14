from flask import request
from flask_restful import Resource

from utility.api import api
from controller.c_analytics import getAnalyticsGeneralAnalytics, getPopularAnalytics
from controller.c_analytics import getPopularAnalyticsForUser
from controller.c_user import verify_token

class Analytics(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success'] and data['role'] == 1):
                return getAnalyticsGeneralAnalytics()
            elif(data['success'] and data['role'] == 3):
                return {
                    "success":True,
                }
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }

class PopularAnalytics(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        user = request.args.get('user')
        print("user " ,  user)
        if(token):
            data = verify_token(token)
            if(data["success"] and (data["role"] == 1 or data["role"] == 3) and user):
                return getPopularAnalyticsForUser(data["id"])
            elif(data['success'] and data['role'] == 1):
                return getPopularAnalytics()
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }


api.add_resource(Analytics, '/api/analytics')
api.add_resource(PopularAnalytics, '/api/popular_analytics')