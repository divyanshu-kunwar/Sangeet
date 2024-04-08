import datetime

from utility.model import db, Song , Album, Flagged , audioData, Tag, User

# ================================== SONG ===============================================

def get_all_songs():
    songs = []
    for song in Song.query.all():
        songs.append({
            "id": song.id,
            "name": song.name,
            "image": song.image,
            "created_at": str(song.created_at.strftime("%d-%B-%Y")),
            "tags": [tag.name for tag in song.tags],
            "albums": [album.name for album in song.albums],
            "creators": [user.name for user in song.creators],
            "play_count": song.play_count,
            "like_count": song.like_count
        })
    return songs

def addSong(name: str, image:str,albums_id: list,tags_id: list, creators_id: list , audio , lyrics:str) -> dict:
    try:
        song=Song(name=name, created_at=datetime.datetime.now() , image=image)
        db.session.add(song)
        for tag_id in tags_id:
            tag = Tag.query.filter_by(id=tag_id).first()
            if tag:
                song.tags.append(tag)
        for album_id in albums_id:
            album = Album.query.filter_by(id=album_id).first()
            if album:
                song.albums.append(album)
        for creator_id in creators_id:
            user = User.query.filter_by(id=creator_id).first()
            if user:
                song.creators.append(user)
        db.session.add(song)
        # store audioData to database
        audio = audioData(song_id=song.id, lyrics=lyrics, audio=audio)
        db.session.add(audio)
        db.session.commit()
        return {
            "success": True,
            "id": song.id,
            "message": "Song added successfully"
        }
    except Exception as e:
        print("c_song->addSong", e)
        return {
            "success": False,
            "message": "Failed to add song",
        }

def getSong(song_id : int):
    song = Song.query.filter_by(id=song_id).first()
    audio = audioData.query.filter_by(song_id=song_id).first()
    lyrics = audio.lyrics

    return {
        "success": True,
        "id": str(song.id),
        "name": song.name,
        "image": song.image,
        "created_at": str(song.created_at.strftime("%d-%B-%Y")),
        "tags": [{
            "id": tag.id,
            "name": tag.name
        } for tag in song.tags],
        "albums": [{
            "id": album.id,
            "name": album.name,
            "image": album.image,
            "creators": " ".join([creator.name for creator in song.creators]),
        } for album in song.albums],
        "artists": [{
            "id": user.id,
            "name": user.name,
        } for user in song.creators],
        "play_count": song.play_count,
        "like_count": song.like_count,
        "lyrics": lyrics
    }

def get_song_by_creator(email : str):
    # if someone is creator of the song
    songs = []
    user = User.query.filter_by(email=email).first()
    for song in user.songs:
        songs.append({
            "id": song.id,
            "name": song.name,
            "image": song.image,
            "created_at": str(song.created_at.strftime("%d-%B-%Y")),
            "tags": [tag.name for tag in song.tags],
            "albums": [album.name for album in song.albums],
            "creators": [user.name for user in song.creators],
            "play_count": song.play_count,
            "like_count": song.like_count
        })
    return songs

def updateSong(id: int, name: str, image:str, albums_id: list,tags_id: list, creators_id: list,
               lyrics:str) -> dict:
    song = Song.query.filter_by(id=id).first()
    if(song):
        audio = audioData.query.filter_by(song_id=id).first()
        audio.lyrics = lyrics
        db.session.add(audio)
        song.name = name
        song.image = image
        for tag_id in tags_id:
            tag = Tag.query.filter_by(id=tag_id).first()
            if tag and tag not in song.tags:
                song.tags.append(tag)
        for album_id in albums_id:
            album = Album.query.filter_by(id=album_id).first()
            if album and album not in song.albums:
                song.albums.append(album)
        for creator_id in creators_id:
            user = User.query.filter_by(id=creator_id).first()
            if user and user not in song.creators:
                song.creators.append(user)
        db.session.add(song)
        db.session.commit()
        return {
            "success": True,
            "message": "Song updated successfully"
        }
    return {
        "success": False,
        "message": "Failed to update song"
    }

def deleteSong(id: int , email: str) -> dict:
    song = Song.query.filter_by(id=id).first()
    if(song):
        user = User.query.filter_by(email=email).first()
        if user not in song.creators:
            return {
                "success": False,
                "message": "You are not allowed to delete this song"
            }
        audio = audioData.query.filter_by(song_id=id).first()
        if audio:
            db.session.delete(audio)
            
        db.session.delete(song)
        db.session.commit()
        return {
            "success": True,
            "message": "Song deleted successfully"
        }
    return {
        "success": False,
        "message": "Failed to delete song"
    }

def searchSong(query : str) -> dict:
    # search in lyrics in audioData and name in song
    try:
        songs = Song.query.filter(Song.name.ilike('%'+query+'%')).all()
        return {
            "success": True,
            "data": [{
                "id": song.id,
                "name": song.name,
                "creators": " ".join([creator.name for creator in song.creators]),
                "image": song.image
            } for song in songs]
        }
    except Exception as e:
        print("c_song->searchSong", e)
        return {
            "success": False,
            "message": "Failed to search song"
        }

def getPopularSongs(totalRes : int) -> dict:
    try:
        songs = Song.query.all()
        songs_sorted = []
        for song in songs:
            day_since_creation = (datetime.datetime.now() - song.created_at).days
            ratio = (song.like_count * 1) + (song.play_count * 0.2) - (day_since_creation * 2)
            songs_sorted.append((song,ratio))
        songs_sorted.sort(key=lambda x: x[1], reverse=True)
        totalRes = totalRes if totalRes <= len(songs_sorted) else len(songs_sorted)
        filtered_song = [song[0] for song in songs_sorted[:totalRes]]
        return {
            "success": True,
            "data": [{
                "id": song.id,
                "name": song.name,
                "creators": " ".join([creator.name for creator in song.creators]),
                "image": song.image
            } for song in filtered_song]
        }
    except Exception as e:
        print("c_song->getPopularSongs", e)
        return {
            "success": False,
            "message": "Failed to get popular songs"
        }
    
def getLatestSongs(totalRes : int) -> dict:
    try:
        songs = Song.query.all()
        songs_sorted = sorted(songs, key=lambda x: x.created_at, reverse=True)
        totalRes = totalRes if totalRes <= len(songs_sorted) else len(songs_sorted)
        filtered_song = songs_sorted[:totalRes]
        return {
            "success": True,
            "data": [{
                "id": song.id,
                "name": song.name,
                "creators": " ".join([creator.name for creator in song.creators]),
                "image": song.image
            } for song in filtered_song]
        }
    except Exception as e:
        print("c_song->getLatestSongs", e)
        return {
            "success": False,
            "message": "Failed to get latest songs"
        }
    
def increasePlayCount(id: int) -> dict:
    try:
        song = Song.query.filter_by(id=id).first()
        if(song):
            song.play_count += 1
            db.session.commit()
    except Exception as e:
        print("c_song->increasePlayCount", e)
        return {
            "success": False
        }

def toggleSongLike(id: int , email: str) -> dict:
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            song = Song.query.filter_by(id=id).first()
            if song:
                liked = False
                if user in song.liked_by:
                    song.liked_by.remove(user)
                    liked = False
                    song.like_count -= 1
                else:
                    song.liked_by.append(user)
                    liked = True
                    song.like_count += 1
                db.session.add(song)
                db.session.commit()
                return {
                    "success": True,
                    "liked": liked,
                    "like_count": song.like_count
                }
    except Exception as e:
        print("c_song->toggleSongLike", e)
        return {
            "success": False
        }

def checkIsLiked(id: int , email: str) -> dict:
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            song = Song.query.filter_by(id=id).first()
            if song:
                if user in song.liked_by:
                    return True
        return False
    except Exception as e:
        print("c_song->checkIsLiked", e)
        return False
    
