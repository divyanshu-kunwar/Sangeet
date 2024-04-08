from utility.model import db , Tag , User

def getTag(id: int) -> dict:
    try:
        tag = Tag.query.filter_by(id=id).first()
        return {
            "id": tag.id,
            "name": tag.name,
            "image": tag.image
        }
    except:
        return {
            "success":False
        }

def getAllTags():
    try:
        tags = []
        for tag in Tag.query.all():
            tags.append({
                "id": tag.id,
                "name": tag.name,
                "image": tag.image
            })
        
        return tags
    except:
        return {
            "success":False
        }
        
def addTag(name: str , image:str) -> dict:
    try:
        tag = Tag(name=name , image=image)
        db.session.add(tag)
        db.session.commit()
        return {
            "success":True,
            "id": tag.id
        }
    except Exception as e:
        print("c_tag->addTag", e)
        return {
            "success":False
        }

def deleteTag(id: int) -> dict:
    try:
        tag = Tag.query.filter_by(id=id).first()
        db.session.delete(tag)
        db.session.commit()
        return {
            "success":True
        }
    except:
        return {
            "success":False
        }

def updateTag(id: int , name: str , image: str) -> dict:
    try:
        tag = Tag.query.filter_by(id=id).first()
        tag.name = name
        tag.image = image
        db.session.commit()
        return {
            "success":True
        }
    except Exception as e:
        print("c_tag->updateTag", e)
        return {
            "success":False
        }
        
def getTagDetail(id: int) -> dict:
    try:
        tag = Tag.query.filter_by(id=id).first()
        # get all the songs that have this tag
        return {
            "id": tag.id,
            "name": tag.name,
            "image": tag.image,
            "songs": [{
                "id": song.id,
                "name": song.name,
                "image": song.image,
                "artists": "".join([creator.name for creator in song.creators])
            } for song in tag.songs],
            "albums" : [{
                "id": album.id,
                "name": album.name,
                "image": album.image,
                "creator": User.query.get(album.album_creator).name if album.album_creator else None,
            } for album in tag.albums ]
        }
    except Exception as e:
        print("c_tag->getTagDetail", e)
        return {
            "success":False
        }