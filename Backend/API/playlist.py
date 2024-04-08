from flask import request
from flask_restful import Resource

from utility.api import api
from controller.c_playlist import createPlaylist, deletePlaylist, editPlaylist, getPlaylist, getPlaylistAll
from controller.c_user import verify_token

class Playlist(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        id = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                return getPlaylist(id=id, email=data['email'])
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
        name = request.json.get('name')

        if(token):
            data = verify_token(token)
            if(data['success']):
                return createPlaylist(name=name, user_email=data['email'])
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }
    
    def delete(self):
        token = request.headers.get('Authorization')
        id = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                return deletePlaylist(id=id, email=data['email'])
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }
    
    def put(self):
        token = request.headers.get('Authorization')
        id = request.json.get('id')
        name = request.json.get('name') or None
        song_id_to_add = request.json.get('song_id_to_add') or None
        song_id_to_remove = request.json.get('song_id_to_remove') or None

        if(token):
            data = verify_token(token)
            if(data['success']):
                return editPlaylist(id=id,
                                    name=name, 
                                    song_id_to_add=song_id_to_add, 
                                    song_id_to_remove=song_id_to_remove, 
                                    email=data['email'])
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }
    
class AllPlaylist(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success']):
                return getPlaylistAll(email=data['email'])
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }


api.add_resource(Playlist, '/api/playlist')
api.add_resource(AllPlaylist, '/api/playlist_all')