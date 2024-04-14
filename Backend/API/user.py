from flask import request
import re
from flask_restful import Resource

from utility.api import api
from utility.image import resize_image_base64
from utility.image import resize_image_base64
from controller.c_user import check_email_exist , createUser, send_verification
from controller.c_user import create_token, LogIn , getPopularArtist, updatePassword, editDetail
from controller.c_user import verify_otp, reset_password, set_OTP, verify_token
from controller.c_user import get_user_private_details, get_all_user_detail, getArtistDetail
from utility.model import Role , User as UserModel

# ===================================================== Helper Functions =====================================


def verify_name(name : str):
    if((not name) or len(name) < 3):
        return {
            "success":False,
            "message": "❌ Name is too short \n"
        }
    elif(len(name) > 30):
        return {
            "success":False,
            "message": "❌ Name is too long"
        }
    else:
        return {
            "success":True,
            "message": "✔️ Name is as per specification \n"
        }

def verify_email(email : str, checkExist=False):
    if(checkExist and email and check_email_exist(email)):
        return {
            "success":False,
            "message": "❌ Email already exist \n "
        }
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(email and re.fullmatch(regex, email)):
        return {
            "success":True,
            "message": "✔️ Email is as per specification \n "
        }
    return {
        "success":False,
        "message": "❌ Email is invalid \n"
    }
    
def verify_password(password : str):
    if((not password) or len(password) < 8):
        return {
            "success":False,
            "message": "❌ Password must be at least 8 characters \n"
        }
    else:
        return {
            "success":True,
            "message": "✔️ Password is as per specification \n"
        }

def verify_role(role : str):
    role_ = Role.query.filter_by(name=role).first()
    if(role_):
        return {
            "success":True,
            "message": "✔️ Type : " + role + " account \n"
        }
    else:
        return {
            "success":False,
            "message": "❌ Invalid role \n"
        }

def verify_code(code : str):
    if((not code) or len(code) != 6):
        return {
            "success":False,
            "message": "❌ Invalid code \n"
        }
    else:
        return {
            "success":True,
            "message": "✔️ Code is as per specification \n"
        }


# ===================================================== API Classes =====================================

class Register(Resource):
    def __init__(self):
        pass
    def post(self):
        name = request.json.get('name')
        email = request.json.get('email')
        email = email.lower()
        password = request.json.get('password')
        role = request.json.get('role')
        image = request.json.get('image')
        if(image):
            image = resize_image_base64(image)

        name_verification = verify_name(name)
        email_verification = verify_email(email, checkExist=True)
        password_verification = verify_password(password)
        role_verification = verify_role(role)

        status = name_verification['success'] and email_verification['success'] and password_verification['success'] and role_verification['success']
        messages = name_verification['message'] + email_verification['message'] + password_verification['message'] + role_verification['message']

        if(status):
            created_user = createUser(name=name, email=email, password=password , image=image , role=role)
            if(created_user['success']):
                print("======================== Created =======================")
                verification_sent = send_verification(email, created_user['verification_code'], name)
                print("======================== Mail Sent =======================")
                if(verification_sent['success']):
                    return {
                        "success":True,
                        "message": messages + "✔️ Sent verification email to " + email + "\n"
                    }

        return {
            "success":False,
            "message": messages
        }

class VerifyOTP(Resource):
    def __init__(self):
        pass
    def post(self):
        code = request.json.get('code')
        email = request.json.get('email')
        email = email.lower()
        
        code_verification = verify_code(code)
        email_verification = verify_email(email)

        status = code_verification['success'] and email_verification['success']

        if(status):
            print("It is status true")
            created_user = verify_otp(email, code )
            if(created_user['success']):
                return {
                    "success":True,
                    "message": "✔️ Verified Successfully\n",
                    "token" : create_token(email)
                }

        print("It is false uff")
        return {
            "success":False,
            "message": "❌ Wrong OTP \n"
        }

class Login(Resource):
    def __init__(self):
        pass
    def post(self):
        email = request.json.get('email')
        email = email.lower()
        password = request.json.get('password')


        email_verification = verify_email(email)
        password_verification = verify_password(password)


        status = email_verification['success'] and password_verification['success']
        message = email_verification['message'] + password_verification['message']

        if(status):
            loggedIn = LogIn(email, password)
            # check if a token is in database
            user = UserModel.query.filter_by(email=email).first()
            if(loggedIn['success']):
                token = user.JWTtoken
                verify = verify_token(token)
                if(not verify['success']):
                    token = create_token(email)
                return {
                    "success":True,
                    "message": "✔️ Logged in \n",
                    "token" : token
                }
            else:
                return {
                    "success":False,
                    "message": loggedIn['message']
                }

        return {
            "success":False,
            "message": message
        }

class SendOTP(Resource):
    def __init__(self):
        pass
    def post(self):
        email = request.json.get('email')
        email = email.lower()

        user_detail = set_OTP(email)
        if(user_detail['success']):
            sent_verification = send_verification(user_detail['email'], user_detail['verification_code'], user_detail['name'])
            if(sent_verification['success']):
                return {
                    "success":True,
                    "message": "✔️ Sent verification email to " + user_detail['email'] + "\n"
                }  

        return {
            "success":False,
            "message": "❌ User does not exist \n"
        }

class VerifyOTP2(Resource):
    def __init__(self):
        pass
    def post(self):
        code = request.json.get('code')
        email = request.json.get('email')
        email = email.lower()
        new_password = request.json.get('password')


        code_verification = verify_code(code)
        email_verification = verify_email(email)
        password_verification = verify_password(new_password)

        status = code_verification['success'] and email_verification['success'] and password_verification['success']
        message = code_verification['message'] + email_verification['message'] + password_verification['message']

        if(status):
            verified_user = verify_otp(email, code)
            if(verified_user['success']):
                if(reset_password(email, new_password)):
                    return {
                        "success":True,
                        "message": "✔️ Verified Successfully\n",
                        "token": create_token(email)
                    }
            else:
                return {
                    "success":False,
                    "message": "❌ Wrong OTP \n"
                }
        return {
            "success":False,
            "message": message
        }

class User(Resource):
    def __init__(self):
        pass

    def get(self):
        # from authorization
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success']):
                # get the complete detail of user
                user_detail = get_user_private_details(data['email'])
                if(user_detail['success']):
                    return user_detail
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
        new_name = request.json.get('name')
        new_image = request.json.get('image')
        isArtist = request.json.get('isCreator')

        if(new_image):
            new_image = resize_image_base64(new_image)

        old_password = request.json.get('oldPassword')
        new_password = request.json.get('newPassword')
        if(token):
            data = verify_token(token)
            if(data['success']):
                if(old_password):
                    return updatePassword(data['email'], old_password, new_password)
                else:
                    return editDetail(data["email"], new_name, new_image , isArtist)
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }
                    
class UserAll(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success'] and data['role']==1):
                all_user_detail = get_all_user_detail()
                return {
                    "success":True,
                    "users": all_user_detail['data']
                }
            else:
                return {
                    "success":False,
                    "message": "❌ Require admin token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }
                
class CreatorAll(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success'] and data['role'] in [1,3]):
                all_user_detail = get_all_user_detail()
                # only users who is admin or creator
                filt_users = list(filter(lambda x: x['role'] in ["admin","creator"] , all_user_detail['data']))
                return {
                    "success":True,
                    "artists": filt_users
                }
            else:
                return {
                    "success":False,
                    "message": "❌ Require admin token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }

class popularArtists(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        n = int(request.args.get('n'))
        if(token):
            data = verify_token(token)
            if(data['success']):
                return getPopularArtist(n)
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }
    
class Artists(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        id = request.args.get('id')
        if(token):
            data = verify_token(token)
            if(data['success']):
                return getArtistDetail(id)
            else:
                return {
                    "success":False,
                    "message": "❌ Invalid token \n"
                }
        return {
            "success":False,
            "message": "❌ token not found\n"
        }

class VerifyToken(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        if(token):
            data = verify_token(token)
            if(data['success'] and data['role'] == 1):
                return {
                    "valid" : True,
                    "admin" : True,
                    "creator" : False
                }
            elif(data['success'] and data['role'] == 3):
                return {
                    "valid" : True,
                    "admin" : False,
                    "creator" : True
                }
            elif(data['success']):
                return {
                    "valid" : True,
                    "admin" : False,
                    "creator" : False
                }
            else:
                return {
                    "valid" : False,
                    "admin" : False,
                    "creator" : False
                }

api.add_resource(VerifyToken, '/api/verify')
api.add_resource(Register, '/api/register')
api.add_resource(VerifyOTP, '/api/verify_otp')
api.add_resource(Login, '/api/login')

api.add_resource(VerifyOTP2, '/api/verify_otp2')
api.add_resource(SendOTP, '/api/request_otp')

api.add_resource(User, '/api/user')
api.add_resource(UserAll, '/api/all_users')
api.add_resource(CreatorAll, '/api/all_creators')
api.add_resource(popularArtists, '/api/popularArtists')
api.add_resource(Artists, '/api/artist')



