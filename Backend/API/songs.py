from flask import request
from flask_restful import Resource
import json
from utility.api import api
from controller.c_user import verify_token
from controller.c_song import get_all_songs , get_song_by_creator , addSong , deleteSong , getSong , updateSong
from controller.c_song import getPopularSongs , getLatestSongs , toggleSongLike , checkIsLiked
from utility.image import resize_image_base64

class AllSong(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success']):
                all_song = get_all_songs()
                return {
                    "success":True,
                    "songs": all_song
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
    
class UserSongs(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success']):
                all_song = get_song_by_creator(data['email'])
                return {
                    "success":True,
                    "songs": all_song
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
    
class Songs(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        id = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                return getSong(id)
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
        name = request.form.get('name')
        image = request.form.get('image')
        if(image):
            image = resize_image_base64(image)
        albums = request.form.get('albums') or []
        creators = json.loads(request.form.get('artists'))
        tags = json.loads(request.form.get('tags'))
        lyrics = request.form.get('lyrics')
        audio = request.files['audio']
        audioData = audio.read()
        if(token):
            data = verify_token(token)
            if(data['success']):
                if(data['role'] in [1,3]):
                    return addSong(name=name, image=image, albums_id=albums, 
                                   creators_id=creators, tags_id=tags, audio=audioData , lyrics=lyrics)
                else:
                    return {
                        "success":False,
                        "message": "❌ You are not authorized to add songs \n"
                    }
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":True,
            "message": "❌ token not found\n"
        }
    
    def put(self):
        token = request.headers.get('Authorization')
        id = request.json.get('id')
        name = request.json.get('name')
        image = request.json.get('img')
        if(image):
            image = resize_image_base64(image)
        albums = request.json.get('albums') or []
        creators = request.json.get('artists')
        tags = request.json.get('tags')
        lyrics = request.json.get('lyrics')
        if(token):
            data = verify_token(token)
            if(data['success']):
                if(data['role'] in [1,3]):
                    return updateSong(id=id, name=name, image=image, albums_id=albums, 
                                   creators_id=creators, tags_id=tags, lyrics=lyrics)
                else:
                    return {
                        "success":False,
                        "message": "❌ You are not authorized to update songs \n"
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
    
    def delete(self):
        token = request.headers.get('Authorization')
        id = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                if(data['role'] in [1,3]):
                    return deleteSong(id , data['email'])
                else:
                    return {
                        "success":False,
                        "message": "❌ You are not authorized to delete songs \n"
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

class PopularSongs(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        totalRes = int(request.args.get('n'))
        if(token):
            data = verify_token(token)
            if(data['success']):
                return getPopularSongs(totalRes)
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }

class LatestSongs(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        totalRes = int(request.args.get('n'))
        if(token):
            data = verify_token(token)
            if(data['success']):
                return getLatestSongs(totalRes)
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }

class Like(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        song_id = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                isliked = checkIsLiked(song_id, data['email'])
                return {
                    "success":True,
                    "isliked": isliked
                }
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
            
    def post(self):
        token = request.headers.get('Authorization')
        song_id = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                return toggleSongLike(song_id, data['email'])
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }

api.add_resource(AllSong, '/api/all_songs')
api.add_resource(UserSongs, '/api/user_songs')
api.add_resource(Songs , '/api/songs')
api.add_resource(PopularSongs, '/api/popularSongs')
api.add_resource(LatestSongs, '/api/latestSongs')
api.add_resource(Like, '/api/like')



