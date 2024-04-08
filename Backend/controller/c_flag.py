import datetime
from utility.model import db, Flagged, Song , User
from flask import current_app , render_template
from utility.mailer import Mail

def get_flagged_items():
    flagged = []
    for flag in Flagged.query.all():
        # get song name and creator name 
        song = Song.query.filter_by(id=flag.song_id).first()
        # get user name and email
        user = User.query.filter_by(id=flag.flagged_by).first()
        flagged.append({
            "id": flag.id,
            "song_name": song.name,
            "song_creators": [user.name for user in song.creators],
            "song_image": song.image,
            "user_name": user.name,
            "user_email": user.email,
            "flagged_at": str(flag.flag_created_at.strftime("%d-%B-%Y")),
            "reason" : flag.reason
        })
    return flagged

def addFlag(song_id: int, email: str, reason : str) -> dict:
    try:
        user = User.query.filter_by(email=email).first()
        flag = Flagged(song_id=song_id, flagged_by=user.id, 
                flag_created_at=datetime.datetime.now(), reason=reason)
        db.session.add(flag)
        db.session.commit()
        return {
            "success":True
        }
    except Exception as e:
        print("c_flag->addFlag",e)
        return {
            "success":False
        }
    
def resolveFlag(id: int , resolved:bool) -> dict:
    try:
        flag = Flagged.query.filter_by(id=id).first()
        song = Song.query.filter_by(id=flag.song_id).first()
        user = User.query.filter_by(id=flag.flagged_by).first()
        # send an email to the user your request is resolved
        data = {
            "song_name": song.name,
            "song_image": song.image,
            "song_creators": [user.name for user in song.creators],
            "user_name": user.name,
            "flagged_at": str(flag.flag_created_at.strftime("%d-%B-%Y")),
            "reason": flag.reason,
            "resolved": resolved
        }
        mail = Mail(current_app)
        msg_string = render_template('flag.html', data=data)
        mail.send(subject="Issue resolved", to_email=user.email, htmlbody=msg_string)
        db.session.delete(flag)
        db.session.commit()
        return {
            "success":True
        }
    except Exception as e:
        print("c_flag->resolveFlag",e)
        return {
            "success":False
        }

def isResolved(songId: str, email: str) -> bool:
    user = User.query.filter_by(email=email).first()
    flag = Flagged.query.filter_by(song_id=songId, flagged_by=user.id).first()
    if flag:
        return False
    return True