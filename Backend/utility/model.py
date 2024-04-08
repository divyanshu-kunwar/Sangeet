from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_songs = db.Table('user_song',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
    db.Column('song_id', db.Integer(), db.ForeignKey('song.id'), primary_key=True)
)

user_liked_songs = db.Table('user_liked_song',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
    db.Column('song_id', db.Integer(), db.ForeignKey('song.id'), primary_key=True)
)

album_song = db.Table('album_song',
    db.Column('album_id', db.Integer(), db.ForeignKey('album.id'), primary_key=True),
    db.Column('song_id', db.Integer(), db.ForeignKey('song.id'), primary_key=True)
)

album_tag = db.Table('album_tag',
    db.Column('album_id', db.Integer(), db.ForeignKey('album.id'), primary_key=True),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'), primary_key=True)
)

song_tag = db.Table('song_tag',
    db.Column('song_id', db.Integer(), db.ForeignKey('song.id'), primary_key=True),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'), primary_key=True)
)

playlist_songs = db.Table('playlist_song',
    db.Column('playlist_id', db.Integer(), db.ForeignKey('playlists.id'), primary_key=True),
    db.Column('song_id', db.Integer(), db.ForeignKey('song.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    JWTtoken = db.Column(db.String, unique=True, nullable=True)
    verification_code = db.Column(db.String, unique=True, nullable=True)
    image = db.Column(db.String, unique=False, nullable=True)
    profile_view_count = db.Column(db.Integer, default=0, nullable=False)
    joined_on = db.Column(db.DateTime, nullable=False)
    last_visit = db.Column(db.DateTime, nullable=True)
    image = db.Column(db.String, unique=False, nullable=True)
    isbanned = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    Albums = db.relationship('Album', backref='User', lazy=True)
    LikedSongs = db.relationship('Song', secondary=user_liked_songs, lazy='subquery', backref=db.backref('liked_by', lazy=True))
    
    def __str__(self):
        return self.name

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    album_creator = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image = db.Column(db.String, unique=False, nullable=True)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    play_count = db.Column(db.Integer, default=0, nullable=False)
    like_count = db.Column(db.Integer, default=0, nullable=False)
    image = db.Column(db.String, unique=False, nullable=True)
    albums = db.relationship('Album', secondary=album_song, lazy='subquery', backref=db.backref('songs', lazy=True))
    creators = db.relationship('User', secondary=user_songs, lazy='subquery', backref=db.backref('songs', lazy=True))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    image = db.Column(db.String, unique=False, nullable=True)
    albums = db.relationship('Album', secondary=album_tag, lazy='subquery', backref=db.backref('tags', lazy=True))
    songs = db.relationship('Song', secondary=song_tag, lazy='subquery', backref=db.backref('tags', lazy=True))

class Flagged(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False )
    flagged_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flag_created_at = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String, unique=False, nullable=True)
    
class audioData(db.Model):
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False , primary_key=True)
    audio = db.Column(db.LargeBinary, nullable=False)
    lyrics = db.Column(db.String, nullable=True)

class notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

class Playlists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Song', secondary=playlist_songs, lazy='subquery', backref=db.backref('playlists', lazy=True))

class ArtistAnalytics(db.Model):
    date_of_data = db.Column(db.DateTime, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    profile_view_count = db.Column(db.Integer, default=0, nullable=False)
    user_play_count = db.Column(db.Integer, default=0, nullable=False)

class SongAnalytics(db.Model):
    date_of_data = db.Column(db.DateTime, nullable=False, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False, primary_key=True)
    song_play_count = db.Column(db.Integer, default=0, nullable=False)
    song_like_count = db.Column(db.Integer, default=0, nullable=False)

class AlbumAnalytics(db.Model):
    date_of_data = db.Column(db.DateTime, nullable=False, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False, primary_key=True)
    album_play_count = db.Column(db.Integer, default=0, nullable=False)

class TagsAnalytics(db.Model):
    date_of_data = db.Column(db.DateTime, nullable=False, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False, primary_key=True)
    tag_play_count = db.Column(db.Integer, default=0, nullable=False)

class GeneralAnalytics(db.Model):
    date_of_data = db.Column(db.DateTime, nullable=False, primary_key=True)
    total_users = db.Column(db.Integer, default=0, nullable=False)
    total_creators = db.Column(db.Integer, default=0, nullable=False)
    total_songs = db.Column(db.Integer, default=0, nullable=False)
    total_albums = db.Column(db.Integer, default=0, nullable=False)
    user_joined_today = db.Column(db.Integer, default=0, nullable=False)
    song_created_today = db.Column(db.Integer, default=0, nullable=False)
    album_created_today = db.Column(db.Integer, default=0, nullable=False)

