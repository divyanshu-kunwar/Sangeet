from utility.model import db, User, Song, Album , Tag , audioData
from utility.model import ArtistAnalytics, SongAnalytics, AlbumAnalytics, TagsAnalytics
from utility.model import GeneralAnalytics
import datetime

def updateAnalyticsAll():
    date_of_data = datetime.datetime.now()
    artists = {}
    songs = {}
    albums = {}
    tags = {}
    last_day_gemeral_analytics = GeneralAnalytics.query.order_by(GeneralAnalytics.date_of_data.desc()).first()
    
    # get all albums id
    for album in Album.query.all():
        albums[album.id] = {
            "album_play_count": 0
        }
    # get all tags id
    for tag in Tag.query.all():
        tags[tag.id] = {
            "tag_play_count": 0
        }
    
    # get all user id
    for user in User.query.all():
        if(user.role == 3):
            artists[user.id] = {
                "profile_view_count": user.profile_view_count,
                "user_play_count": 0
            }

    # get all song id
    for song in Song.query.all():
        songs[song.id] = {
            "song_play_count": song.play_count,
            "song_like_count": song.like_count
        }
        for album in song.albums:
            if album.id in albums:
                albums[album.id]["album_play_count"] += song.play_count
        for tag in song.tags:
            if tag.id in tags:
                tags[tag.id]["tag_play_count"] += song.play_count
        for creator in song.creators:
            artists[song.creators[0].id]["user_play_count"] += song.play_count
    
    # create general analytics
    total_users = len(User.query.all())

    general_analytics = GeneralAnalytics(
        date_of_data = date_of_data,
        total_users = total_users,
        total_creators = len(artists),
        total_songs = len(songs),
        total_albums = len(albums),
        user_joined_today = total_users - last_day_gemeral_analytics.total_users if last_day_gemeral_analytics else total_users,
        song_created_today = len(songs) - last_day_gemeral_analytics.total_songs if last_day_gemeral_analytics else len(songs),
        album_created_today = len(albums) - last_day_gemeral_analytics.total_albums if last_day_gemeral_analytics else len(albums)
    )

    db.session.add(general_analytics)

    # create artist analytics
    for artist_id in artists:
        artist_analytics = ArtistAnalytics(
            date_of_data = date_of_data,
            user_id = artist_id,
            profile_view_count = artists[artist_id]["profile_view_count"],
            user_play_count = artists[artist_id]["user_play_count"]
        )
        db.session.add(artist_analytics)
    
    # create song analytics
    for song_id in songs:
        song_analytics = SongAnalytics(
            date_of_data = date_of_data,
            song_id = song_id,
            song_play_count = songs[song_id]["song_play_count"],
            song_like_count = songs[song_id]["song_like_count"]
        )
        db.session.add(song_analytics)
    
    # create album analytics
    for album_id in albums:
        album_analytics = AlbumAnalytics(
            date_of_data = date_of_data,
            album_id = album_id,
            album_play_count = albums[album_id]["album_play_count"]
        )
        db.session.add(album_analytics)
    
    # create tag analytics
    for tag_id in tags:
        tag_analytics = TagsAnalytics(
            date_of_data = date_of_data,
            tag_id = tag_id,
            tag_play_count = tags[tag_id]["tag_play_count"]
        )
        db.session.add(tag_analytics)

    db.session.commit()

def getAnalyticsForExport():
    # get all the analytics for this month
    pass




