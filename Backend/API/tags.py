from flask import request
from flask_restful import Resource

from utility.api import api
from utility.image import resize_image_base64
from controller.c_tags import getAllTags , addTag , deleteTag , updateTag , getTag, getTagDetail
from controller.c_user import verify_token

class Tags(Resource):
    def __init__(self):
        pass

    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success']):
                return getTag(id=int(request.args.get('id')))
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
        image = request.json.get('image')
        if(image):
            image = resize_image_base64(image)
        
        if(token):
            data = verify_token(token)
            if(data['success']):
                if(data['role'] == 1):
                    return addTag(name=name , image=image)
                else:
                    return {
                        "success":False,
                        "message": "❌ You are not authorized to add tags"
                    }
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token"
                }
        return {
            "success":False,
            "message": "❌ token not found"
        }
    
    def put(self):
        token = request.headers.get('Authorization')
        id = request.json.get('id')
        name = request.json.get('name')
        image = request.json.get('image')
        if(image):
            image = resize_image_base64(image)
        if(token):
            data = verify_token(token)
            if(data['success']):
                if(data['role'] == 1):
                    return updateTag(id=id , name=name , image=image)
                else:
                    return {
                        "success":False,
                        "message": "❌ You are not authorized to update tags"
                    }
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token"
                }
        return {
            "success":False,
            "message": "❌ token not found"
        }
    
    def delete(self):
        token = request.headers.get('Authorization')
        id = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                if(data['role'] == 1):
                    return deleteTag(id=id)
                else:
                    return {
                        "success":False,
                        "message": "❌ You are not authorized to delete tags"
                    }
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token"
                }
        return {
            "success":False,
            "message": "❌ token not found"
        }

class AllCategories(Resource):
    def __init__(self):
        pass

    def get(self):
        return {
            "success":True,
            "tags": getAllTags()
        }

class TagDetail(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success']):
                return getTagDetail(id=int(request.args.get('id')))
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }    

api.add_resource(AllCategories, '/api/all_tags')
api.add_resource(Tags, '/api/tags')
api.add_resource(TagDetail, '/api/tag_detail')