from utility.model import db , Role
from controller.c_user import createUser

def create_initials(action_id=0):
    """
    Recreates the database, adds roles and an admin user, and commits the changes to the database.
    """
    # Recreate Database
    if(action_id==0):
        db.create_all()
        return
    db.drop_all()
    db.create_all()

    # Add roles
    role_admin = Role(name='admin')
    role_user = Role(name='user')
    role_creator = Role(name='creator')
    
    db.session.add(role_admin)
    db.session.add(role_user)
    db.session.add(role_creator)
    db.session.commit()

    # Add admin user
    admin = createUser(name='admin', email='admin@sangeet.com', password='Sangeet@987', role='admin' , image=None)

    if admin['success'] == True:
        print("\n\n 🧑‍💻Admin created with \n\temail: admin@sangeet.com \n\tpassword: Sangeet@987 \n\n")

