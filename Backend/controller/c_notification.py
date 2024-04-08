import datetime
from utility.model import db, notifications

def addNotification(user_id: int, message: str) -> dict:
    try:
        notification = notifications(user_id=user_id, message=message, created_at=datetime.datetime.now())
        db.session.add(notification)
        db.session.commit()
        return True
    except Exception as e:
        print("c_notification->addNotification", e)
        return False
    
def getNotifications(user_id: int) -> dict:
    try:
        notification = notifications.query.filter_by(user_id=user_id).all()
        return {
            "success": True,
            "notifications": [
                {
                    "message": notification.message,
                    "created_at": notification.created_at.strftime("%B,%d %H:%M "),
                    "id": notification.id
                } for notification in notification
            ]
        }
    except Exception as e:
        print("c_notification->getNotifications", e)
        return {
            "success": False
        }
    
def deleteNotification(id : int , user_id : int) -> dict:
    try:
        notification = notifications.query.filter_by(id=id, user_id=user_id).first()
        if(notification):
            db.session.delete(notification)
            db.session.commit()
            return {
                "success": True,
                "message": "Notification deleted successfully"
            }
        else:
            return {
                "success": False,
                "message": "Notification not found"
            }
    except Exception as e:
        print("c_notification->deleteNotification", e)
        return {
            "success": False
        }