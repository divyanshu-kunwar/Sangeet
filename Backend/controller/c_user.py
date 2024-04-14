import random
import hashlib
import jwt 
from flask import current_app , render_template
import datetime
from utility.cache import cache


from utility.model import db , User , Role
from utility.mailer import Mail

def generate_verification_code() -> int:
    return random.randint(100000, 999999)

def check_email_exist(email: str) -> bool:
    """
    Check if the email exists in the database.

    Args:
    email (str): The email to be checked.

    Returns:
    bool: True if the email exists, False otherwise.
    """
    user = User.query.filter_by(email=email).first()
    if user:
        if(user.verification_code != None):
            return False
        return True
    return False

def createUser(name: str, email: str, password: str,image: str, role: str = 'user') -> dict:
    """
    Create a new user in the database.

    Args:
    name (str): The name of the user.
    email (str): The email of the user.
    password (str): The password of the user.
    role (str, optional): The role of the user. Defaults to 'user'.

    Returns:
    dict: A dictionary indicating the success of the operation and any error messages.
    """

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    current_date = datetime.datetime.now()

    if(role != 'admin'):
        verification_code = generate_verification_code()
    else:
        verification_code = None

    role = Role.query.filter_by(name=role).first()
    role = role.id

    # delete previous record if verifcation code exist
    user = User.query.filter_by(email=email).first()
    if(user):
        db.session.delete(user)
        db.session.commit()

    user = User(name=name, email=email, password=hashed_password, role=role, verification_code=verification_code,
                profile_view_count=0,joined_on=current_date, image=image)
    try:
        db.session.add(user)
        db.session.commit()
            
        return {
            "success":True,
            "verification_code": verification_code,
            "name": name,
            "email": email
        }
    except Exception as e:
        print("c_user->createUser", e)
        return {
            "success":False,
        }
    
def send_verification(email: str, verification_code: int, name: str) -> dict:
    mail = Mail(current_app)
    msg_string = render_template('code_verification.html', code=verification_code , name=name)
    result = mail.send(subject="Verification Code", to_email=email, 
        htmlbody=msg_string)
    if(result == False):
        return {
            "success":False
        }
    else:
        return {
            "success":True
        }

def verify_otp(email: str, code: int) -> dict:
    user = User.query.filter_by(email=email).first()
    if(user.verification_code == code):
        print("It is true ooooooooo")
        user.verification_code = None
        db.session.commit()
        return {
            "success":True
        }
    else:
        return {
            "success":False
        }

def LogIn(email: str, password: str) -> dict:
    user = User.query.filter_by(email=email).first()
    if(user):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if(hashed_password == user.password):
            return {
                "success":True
            }
        else:
            return {
                "success":False,
                "message": "❌ Wrong password \n"
            }
    else:
        return {
            "success":False,
            "message": "❌ User does not exist \n"
        }

def reset_password(email: str, new_password: str) -> dict:
    user = User.query.filter_by(email=email).first()
    if(user):
        hashed_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        user.password = hashed_password
        db.session.commit()
        return {
            "success":True
        }
    return {
        "success":False
    }

def set_OTP(email: str ) -> dict:
    user = User.query.filter_by(email=email).first()
    if(user):
        code = generate_verification_code()
        user.verification_code = code
        db.session.commit()
        return {
            "success":True,
            "verification_code": code,
            "name": user.name,
            "email": user.email
        }
    return {
        "success":False
    }

def create_token(email: str, days=7) -> dict:

    exp = datetime.datetime.now() + datetime.timedelta(days=days)
    user = User.query.filter_by(email=email).first()

    token = jwt.encode({
        'email': email,
        'role': user.role,
        'exp': exp
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    user.JWTtoken = token
    db.session.commit()

    return token

@cache.memoize(timeout=3600)
def verify_token(token: str) -> dict:
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        # get email , role and expiration
        email = data['email']
        role = data['role']
        exp = data['exp']

        if(exp < datetime.datetime.now().timestamp()):
            return {
                "success":False
            }
        # update user last_visit
        user = User.query.filter_by(email=email).first()
        user.last_visit = datetime.datetime.now()
        db.session.commit()
        return {
            "success":True,
            "email": email,
            "role": role,
            "id": user.id
        }
    except Exception as e:
        print("c_user->verify_token", e)
        return {
            "success":False
        }

def get_user_private_details(email: str) -> dict:
    user = User.query.filter_by(email=email).first()
    if(user):
        role = Role.query.filter_by(id=user.role).first()
        return {
            "success":True,
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "image": user.image,
            "profile_view_count": user.profile_view_count,
            "joined_on": str(user.joined_on),
            "role": role.name.capitalize()
        }
    return {
        "success":False
    }

@cache.memoize(timeout=120)
def get_user_public_details(userid: int) -> dict:
    user = User.query.filter_by(id=userid).first()
    if(user):
        return {
            "success":True,
            "id": user.id,
            "name": user.name,
            "image": user.image,
            "profile_view_count": user.profile_view_count,
            "joined_on": str(user.joined_on)
        }
    return {
        "success":False
    }

def get_all_user_detail() -> dict:
    users = User.query.all()
    roles = Role.query.all()
    roles_list = ['']
    for role in roles:
        roles_list.append(role)
    data = []
    for user in users:
        role = roles_list[user.role].name
        data.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "image":user.image,
            "role": role,
            "joined_on": str(user.joined_on.strftime("%d-%B-%Y")),
            "profile_view_count": user.profile_view_count,
            "isbanned": user.isbanned
        })
    return {
        "success":True,
        "data": data
    }

def SearchArtist(query: str) -> dict:
    try:
        users = User.query.filter(User.name.like(f'%{query}%')).all()
        data = []
        for user in users:
            data.append({
                "id": user.id,
                "name": user.name,
                "image": user.image
            })
        return {
            "success":True,
            "data": data
        }
    except Exception as e:
        print("c_user->SearchArtist", e)
        return {
            "success":False,
            "message": "Failed to search artist"
        }

@cache.memoize(timeout=60)
def getPopularArtist(totalRes : int) -> dict :
    try:
        artists = User.query.filter(User.role == 3).all()
        data = []
        for artist in artists:
            # no of songs
            if(len(artist.songs)<1):
                continue
            popularity = 2 * artist.profile_view_count - (datetime.datetime.now() - artist.joined_on).days
            data.append({
                "id": artist.id,
                "name": artist.name,
                "image": artist.image,
                "popularity": popularity
            })
        totalRes = totalRes if totalRes <= len(data) else len(data)
        data = sorted(data, key=lambda x: x['popularity'], reverse=True)[:totalRes]
        return {
            "success":True,
            "artists" : data
        }
    except Exception as e:
        print("c_user->getPopularArtist", e)
        return {
            "success":False,
            "message": "Failed to get popular artist"
        }

@cache.memoize(timeout=300)
def getArtistDetail(id : int) -> dict:
    try:
        artist = User.query.get(id)
        artist.profile_view_count += 1
        db.session.commit()
        songs = artist.songs
        albums = artist.Albums

        return {
            "success":True,
            "data": {
                "id": artist.id,
                "name": artist.name,
                "image": artist.image,
                "profile_view_count": artist.profile_view_count,
                "joined_since" : str(artist.joined_on.strftime("%B-%Y")),
                "total_songs": len(songs),
                "total_albums": len(albums),
                "songs" : [{
                    "id": song.id,
                    "name": song.name,
                    "image": song.image
                } for song in songs],
                "albums" : [{
                    "id": album.id,
                    "name": album.name,
                    "image": album.image
                } for album in albums]
            }
        }
    except Exception as e:
        print("c_user->getArtistDetail", e)
        return {
            "success":False,
            "message": "Failed to get artist detail"
        }

def editDetail(email : str , name : str , image:str , role:str):
    try:
        user = User.query.filter_by(email=email).first()
        if(name):
            user.name = name
        if(image):
            user.image = image
        if(role == True):
            user.role = 3
        db.session.commit()
        return {
            "success":True
        }
    except Exception as e:
        print("c_user->editDetail", e)
        return {
            "success":False
        }

def updatePassword(email : str ,oldPassword:str , newPasswoord:str):
    try:
        user = User.query.filter_by(email=email).first()
        if(user):
            hashed_old_pass = hashlib.sha256(oldPassword.encode('utf-8')).hexdigest()
            hashed_new_pass = hashlib.sha256(newPasswoord.encode('utf-8')).hexdigest()
            if(user.password == hashed_old_pass):
                user.password = hashed_new_pass
                db.session.commit()
                return{
                    "success":True
                }
            else:
                return{
                    "success":False,
                    "message": "Old Password is not correct"
                }
        return {
            "success" : False,
            "message" : "User doesn't exist"
        }
    except Exception as e:
        print("c_user->updatPassword", e)
        return {
            "success" : False,
            "message" : "Something Went Wrong"
        }

def getUserNotVisited():
    # get all user whose last visit is more than 24 hours ago
    timenow = datetime.datetime.now()
    users = User.query.all()
    data = []
    for user in users:
        if(user.last_visit is None or timenow - user.last_visit > datetime.timedelta(hours=24)):
            data.append({
                "id": user.id,
                "name": user.name,
                "email": user.email
            })
    return data

