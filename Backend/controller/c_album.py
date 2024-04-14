import datetime
from utility.model import db, Song , Album, Tag, User
from utility.cache import cache

# ============================== ALBUM =====================================================

@cache.memoize(timeout=60)
def get_album(id : int):
    album = Album.query.filter_by(id=id).first()
    return {
        "id": album.id,
        "name": album.name,
        "description": album.description,
        "created_at": str(album.created_at.strftime("%d-%B-%Y")),
        "creator": User.query.get(album.album_creator).name if album.album_creator else None,
        "tags": [{
            "id": tag.id,
            "name": tag.name
        } for tag in album.tags],
        "image": album.image,
        "songs": [{
            "id": song.id,
            "name": song.name,
            "image": song.image,
            "artists": "".join([artist.name for artist in song.creators]) if song.creators else None
        } for song in album.songs]
    }

@cache.memoize(timeout=60)
def get_albums_by_creator(email):
    user = User.query.filter_by(email=email).first()
    albums = Album.query.filter_by(album_creator=user.id).all()
    albums_data = []
    for album in albums:
        albums_data.append({
            "id": album.id,
            "name": album.name,
            "description": album.description,
            "created_at": str(album.created_at.strftime("%d-%B-%Y")),
            "tags": [tag.name for tag in album.tags],
            "image": album.image,
            "songs": [song.name for song in album.songs]
        })

    return albums_data

def addAlbum(name: str, description: str, album_creator_email: str, tags_id: list, 
             songs_id: list, image: str) -> dict:
    try:
        user = User.query.filter_by(email=album_creator_email).first()
        if not user:
            return {
                "success": False,
                "message": "User not found"
            }
        album = Album(name=name, description=description, created_at=datetime.datetime.now(), album_creator=user.id, image=image)
        db.session.add(album)
        for tag_id in tags_id:
            tag = Tag.query.filter_by(id=tag_id).first()
            if tag:
                album.tags.append(tag)
        for song_id in songs_id:
            song = Song.query.filter_by(id=song_id).first()
            if song:
                album.songs.append(song)
        db.session.commit()
        return {
            "success": True,
            "id": album.id,
            "message": "Album added successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Failed to add album",
            "error": str(e)
        }

def updateAlbum(id: int, name: str, description: str, album_creator_email: str, tags_id: list,
                songs_id: list, image: str) -> bool:
    try:
        user = User.query.filter_by(email=album_creator_email).first()
        if not user:
            return False
        album = Album.query.filter_by(id=id).first()
        if not album:
            return False
        album.name = name
        album.description = description
        album.album_creator = user.id
        album.image = image
        db.session.add(album)
        album.tags = []
        album.songs = []
        for tag_id in tags_id:
            tag = Tag.query.filter_by(id=tag_id).first()
            if tag:
                album.tags.append(tag)
        for song_id in songs_id:
            song = Song.query.filter_by(id=song_id).first()
            if song:
                album.songs.append(song)
        db.session.add(album)
        db.session.commit()
        return True
    except Exception as e:
        print("c_album->updateAlbum", e)
        return False

def delete_album(album_id : int, email : str):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            album = Album.query.filter_by(id=album_id).first()
            if album:
                if album.album_creator == user.id:
                    db.session.delete(album)
                    db.session.commit()
                    return True
                else:
                    return False
    except Exception as e:
        print("c_album->delete_album", e)
        return False
    

def searchAlbums(query : str):
    try:
        albums = Album.query.filter(Album.name.ilike('%'+query+'%')).all()
        return {
            "success": True,
            "data": [{
                "id": album.id,
                "name": album.name,
                "image": album.image,
                "creator": User.query.get(album.album_creator).name if album.album_creator else None
            } for album in albums]
        }
    except Exception as e:
        print("c_album->searchAlbums", e)
        return {
            "success": False,
            "message": "Failed to search albums"
        }

@cache.memoize(timeout=60)
def getLatestAlbum(totalRes: int):
    try:
        albums = Album.query.order_by(Album.created_at.desc()).limit(totalRes).all()
        return {
            "success": True,
            "data": [{
                "id": album.id,
                "name": album.name,
                "image": album.image,
                "creator": User.query.get(album.album_creator).name if album.album_creator else None,
                "songs": [{
                    "id": str(song.id),
                    "name": song.name
                } for song in album.songs]
            } for album in albums]
        }
    except Exception as e:
        print("c_album->getLatestAlbum", e)
        return {
            "success": False,
            "message": "Failed to get latest albums"
        }

