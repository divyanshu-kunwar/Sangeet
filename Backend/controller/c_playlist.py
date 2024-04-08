from utility.model import db , Playlists , Song, User

def createPlaylist(name: str, user_email: str) -> dict:
    user = User.query.filter_by(email=user_email).first()
    playlist = Playlists(name=name, user_id=user.id)
    db.session.add(playlist)
    db.session.commit()
    return {
        "success":True,
        "id" : playlist.id
    }

def deletePlaylist(id: int, email: str) -> dict:
    user = User.query.filter_by(email=email).first()
    playlist = Playlists.query.filter_by(id=id).first()
    if playlist.user_id != user.id:
        return {
            "success":False,
            "message": "❌ You don't have permission to delete this playlist"
        }
    if(playlist):
        db.session.delete(playlist)
        db.session.commit()
        return {
            "success":True
        }
    return {
        "success":False
    }

def editPlaylist(id: int, name: str, song_id_to_add: list, song_id_to_remove: list, email: str) -> dict:
    user = User.query.filter_by(email=email).first()
    playlist = Playlists.query.filter_by(id=id).first()
    if playlist.user_id != user.id:
        return {
            "success":False,
            "message": "❌ You don't have permission to edit this playlist"
        }
    if(playlist):
        if(name):
            playlist.name = name
        # add song
        if(song_id_to_add):
            for song_id in song_id_to_add:
                song = Song.query.filter_by(id=song_id).first()
                if song and song not in playlist.songs:
                    playlist.songs.append(song)
        # remove song
        if(song_id_to_remove):
            for song_id in song_id_to_remove:
                song = Song.query.filter_by(id=song_id).first()
                if song and song in playlist.songs:
                    playlist.songs.remove(song)
        db.session.add(playlist)
        db.session.commit()
        return {
            "success":True,
            "message": "✔️ Playlist updated"
        }

def getPlaylist(id: int, email: str) -> dict:
    user = User.query.filter_by(email=email).first()
    playlist = Playlists.query.filter_by(id=id).first()
    if playlist.user_id != user.id:
        return {
            "success":False,
            "message": "❌ You don't have permission to edit this playlist"
        }
    return {
        "success":True,
        "playlist":{
            "id": playlist.id,
            "name": playlist.name,
            "no_of_songs": len(playlist.songs),
            "image": playlist.songs[0].image if len(playlist.songs) > 0 else None,
            "songs": [{
                "id": song.id,
                "name": song.name,
                "image": song.image,
                "created_at": str(song.created_at.strftime("%d-%B-%Y")),
                "creators": ",".join([user.name for user in song.creators]) if song.creators else None,
            } for song in playlist.songs]
        }
    }

def getPlaylistAll(email: str) -> dict:
    user = User.query.filter_by(email=email).first()
    playlists = Playlists.query.filter_by(user_id=user.id).all()
    return {
        "success":True,
        "playlists":[{
            "id": playlist.id,
            "name": playlist.name,
            "no_of_songs": len(playlist.songs),
            "image": playlist.songs[0].image if len(playlist.songs) > 0 else None,
            "songs":[song.id for song in playlist.songs]
        } for playlist in playlists]
    }

