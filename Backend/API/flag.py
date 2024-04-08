from flask import request
from flask_restful import Resource

from utility.api import api
from controller.c_user import verify_token
from controller.c_flag import get_flagged_items , addFlag , resolveFlag , isResolved

class Flagged(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success']):
                all_flagged = get_flagged_items()
                return {
                    "success":True,
                    "songs": all_flagged
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
    
    def post(self):
        token = request.headers.get('Authorization')
        id = request.json.get('id')
        reason = request.json.get('reason')
        if(token):
            data = verify_token(token)
            if(data['success']):
                return addFlag(id, data['email'], reason)
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }
    
class ResolveFlag(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        songId = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                isResolved_ = isResolved(songId , data['email'])
                return {
                    "success":True,
                    "resolved": isResolved_
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
        
    def post(self):
        token = request.headers.get('Authorization')
        id = request.json.get('id')
        resolved = request.json.get('resolved')
        if(token):
            data = verify_token(token)
            if(data['success']):
                return resolveFlag(id, resolved)
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }

api.add_resource(Flagged, '/api/flagged')
api.add_resource(ResolveFlag, '/api/flagged/resolve')
