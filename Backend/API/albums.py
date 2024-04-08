from flask import request
from flask_restful import Resource

from utility.api import api
from controller.c_user import verify_token
from controller.c_album import addAlbum , delete_album, get_album, updateAlbum
from controller.c_album import getLatestAlbum, get_albums_by_creator
from utility.image import resize_image_base64

class UserAlbum(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success']):
                albums = get_albums_by_creator(data['email'])
                return {
                    "success":True,
                    "albums": albums
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
    
class Album(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        id = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                album = get_album(id)
                if(album):
                    return {
                        "success":True,
                        "album": album
                    }
                else:
                    return {
                        "success":False,
                        "message": "❌ Album not found \n"
                    }
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":True
        }
    
    def put(self):
        id = request.json.get('id')
        name = request.json.get('name')
        description = request.json.get('description')
        img = request.json.get('img')
        if(img):
            img = resize_image_base64(img)
        songs = request.json.get('songs')
        token = request.headers.get('Authorization')
        tags = request.json.get('tags')
        if(token):
            data = verify_token(token)
            if(data['success']):
                added = updateAlbum(id=id, name=name , description=description , image=img , songs_id=songs ,
                                  album_creator_email=data['email'], tags_id=tags)
                if(added):
                    return {
                        "success":True,
                        "message" : "✅ Album added successfully \n"
                    }
                else:
                    return {
                        "success":False,
                        "message" : "❌ something went wrong \n"
                    }
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid Token \n"
                }
        return {
            "success":False,
            "message": "❌ Token not found \n"
        }
    
    def delete(self):
        token = request.headers.get('Authorization')
        id = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                deleted = delete_album(id, data['email'])
                if(deleted):
                    return {
                        "success":True,
                        "message": "✅ Album deleted successfully \n"
                    }
                else:
                    return {
                        "success":False,
                        "message": "❌ Not an authorized user \n"
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
        name = request.json.get('name')
        description = request.json.get('description')
        img = request.json.get('img')
        songs = request.json.get('songs')
        token = request.headers.get('Authorization')
        tags = request.json.get('tags')
        if(token):
            data = verify_token(token)
            if(data['success']):
                added = addAlbum(name=name , description=description , image=img , songs_id=songs ,
                                  album_creator_email=data['email'], tags_id=tags)
                if(added):
                    return {
                        "success":True,
                        "message" : "✅ Album added successfully \n"
                    }
                else:
                    return {
                        "success":False,
                        "message" : "❌ something went wrong \n"
                    }
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid Token \n"
                }
        return {
            "success":False,
            "message": "❌ Token not found \n"
        }

class LatestAlbums(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        n = request.args.get('n')
        if(token):
            data = verify_token(token)
            if(data['success']):
                albums = getLatestAlbum(n)
                return {
                    "success":True,
                    "albums": albums
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

api.add_resource(UserAlbum , '/api/user_albums')
api.add_resource(Album, '/api/album')
api.add_resource(LatestAlbums, '/api/latestAlbums')


