from utility.model import db, User, Song, Album , Tag , audioData
from utility.model import ArtistAnalytics, SongAnalytics, AlbumAnalytics, TagsAnalytics
from utility.model import GeneralAnalytics
import datetime
from utility.cache import cache

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
            if creator.id in artists:
                artists[creator.id]["user_play_count"] += song.play_count
    
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

@cache.memoize(timeout=120)
def getAnalyticsGeneralAnalytics():
    users = {
        "date" : [],
        "data" : []
    }
    creators = {
        "date" : [],
        "data" : []
    }
    songs = {
        "date" : [],
        "data" : []
    }
    albums = {
        "date" : [],
        "data" : []
    }

    analytics_all = GeneralAnalytics.query.order_by(GeneralAnalytics.date_of_data.desc()).all()
    last_day = analytics_all[0]
    last_of_last_day = analytics_all[1]

    total_users = last_day.total_users
    total_creators = last_day.total_creators
    total_songs = last_day.total_songs
    total_albums = last_day.total_albums

    del_users = last_day.total_users - last_of_last_day.total_users
    del_creators = last_day.total_creators - last_of_last_day.total_creators
    del_songs = last_day.total_songs - last_of_last_day.total_songs
    del_albums = last_day.total_albums - last_of_last_day.total_albums

    for analytics in analytics_all:
        users["date"].append(analytics.date_of_data.strftime("%Y-%m-%d %H:%M"))
        users["data"].append(analytics.total_users)

        creators["date"].append(analytics.date_of_data.strftime("%Y-%m-%d %H:%M"))
        creators["data"].append(analytics.total_creators)

        songs["date"].append(analytics.date_of_data.strftime("%Y-%m-%d %H:%M"))
        songs["data"].append(analytics.total_songs)

        albums["date"].append(analytics.date_of_data.strftime("%Y-%m-%d %H:%M"))
        albums["data"].append(analytics.total_albums)

    return {
        "success" : True,
        "users" : users,
        "creators" : creators,
        "songs" : songs,
        "albums" : albums,
        "total_users" : total_users,
        "total_creators" : total_creators,
        "total_songs" : total_songs,
        "total_albums" : total_albums,
        "del_users" : del_users,
        "del_creators" : del_creators,
        "del_songs" : del_songs,
        "del_albums" : del_albums
    }

@cache.memoize(timeout=120)
def getPopularAnalytics():
    # get most popular songs , albums , artists and tags
    last_date_of_analytics = GeneralAnalytics.query.order_by(
        GeneralAnalytics.date_of_data.desc()).first().date_of_data
    # get max 5 songs on last day of analytics ordered by play count
    popular_songs_one_day = SongAnalytics.query.filter(
        SongAnalytics.date_of_data == last_date_of_analytics).order_by(
        SongAnalytics.song_play_count.desc()).limit(8).all()
    popular_albums_one_day = AlbumAnalytics.query.filter(
        AlbumAnalytics.date_of_data == last_date_of_analytics).order_by(
        AlbumAnalytics.album_play_count.desc()).limit(8).all()
    popular_artists_one_day = ArtistAnalytics.query.filter(
        ArtistAnalytics.date_of_data == last_date_of_analytics).order_by(
        ArtistAnalytics.user_play_count.desc()).limit(8).all()
    popular_tags_one_day = TagsAnalytics.query.filter(
        TagsAnalytics.date_of_data == last_date_of_analytics).order_by(
        TagsAnalytics.tag_play_count.desc()).limit(8).all()

    songs = []
    albums = []
    artists = []
    tags = []

    # create list of popular songs name , id and image
    for song in popular_songs_one_day:
        song_ = Song.query.get(song.song_id)
        songs.append({
            "id" : song_.id,
            "name" : song_.name,
            "image" : song_.image,
            "play_count" : song.song_play_count,
            "like_count" : song.song_like_count
        })
    
    # create list of popular albums name , id and image
    for album in popular_albums_one_day:
        album_ = Album.query.get(album.album_id)
        albums.append({
            "id" : album_.id,
            "name" : album_.name,
            "image" : album_.image,
            "play_count" : album.album_play_count
        })

    # create list of popular artists name , id and image
    for artist in popular_artists_one_day:
        artist_ = User.query.get(artist.user_id)
        artists.append({
            "id" : artist_.id,
            "name" : artist_.name,
            "image" : artist_.image,
            "play_count" : artist.user_play_count,
            "profile_view_count" : artist.profile_view_count
        })

    # create list of popular tags name , id and image
    for tag in popular_tags_one_day:
        tag_ = Tag.query.get(tag.tag_id)
        tags.append({
            "id" : tag_.id,
            "name" : tag_.name,
            "image" : tag_.image,
            "play_count" : tag.tag_play_count
        })

    return {
        "success" : True,
        "songs" : songs,
        "albums" : albums,
        "artists" : artists,
        "tags" : tags
    }

@cache.memoize(timeout=120)
def getPopularAnalyticsForUser(id : int):
    # get most popular songs , albums, artist and tags which belong to user
    user = User.query.get(id)
    user_song = user.songs
    user_albums = user.Albums
    print(user.name)
    last_date_of_analytics = GeneralAnalytics.query.order_by(
        GeneralAnalytics.date_of_data.desc()).first().date_of_data
    
    # create list of popular songs name , id and image by play_count also date is last_date_of_analytics
    songs_analytics = SongAnalytics.query.filter(
        SongAnalytics.song_id.in_([song.id for song in user_song]),
        SongAnalytics.date_of_data == last_date_of_analytics
    ).limit(20).all()

    # create list of popular albums name , id and image by play_count 
    album_analytics = AlbumAnalytics.query.filter(
        AlbumAnalytics.album_id.in_([album.id for album in user_albums]),
        AlbumAnalytics.date_of_data == last_date_of_analytics
    ).limit(20).all()

    songs = []
    albums = []

    # create list of popular songs name , id and image
    for song in songs_analytics:
        song_ = Song.query.get(song.song_id)
        songs.append({
            "id" : song_.id,
            "name" : song_.name,
            "image" : song_.image,
            "play_count" : song.song_play_count,
            "like_count" : song.song_like_count
        })
    
    # create list of popular albums name , id and image
    for album in album_analytics:
        album_ = Album.query.get(album.album_id)
        albums.append({
            "id" : album_.id,
            "name" : album_.name,
            "image" : album_.image,
            "play_count" : album.album_play_count
        })

        print(songs)
        print(albums)

    return {
        "success" : True,
        "songs" : songs,
        "albums" : albums
    }

@cache.memoize(timeout=120)
def prepareReport(id : int):
    user = User.query.get(id)
    # get all songs, album of user
    user_songs = user.songs
    user_albums = user.Albums

    todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
    last_month_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    # get analytics for these songs between last_month_date and todays_date
    song_analytics = SongAnalytics.query.filter(
        SongAnalytics.song_id.in_([song.id for song in user_songs]),
        SongAnalytics.date_of_data.between(last_month_date, todays_date)
    ).order_by(SongAnalytics.date_of_data.desc()).all()

    # get analytics for these albums between last_month_date and todays_date
    album_analytics = AlbumAnalytics.query.filter(
        AlbumAnalytics.album_id.in_([album.id for album in user_albums]),
        AlbumAnalytics.date_of_data.between(last_month_date, todays_date)
    ).order_by(AlbumAnalytics.date_of_data.desc()).all()

    # group song analytics by song id 
    song_analytics_grouped = {}

    for song in song_analytics:
        if(song.song_id in song_analytics_grouped):
            song_analytics_grouped[song.song_id]["play_count"].append(song.song_play_count)
            song_analytics_grouped[song.song_id]["like_count"].append(song.song_like_count)
            song_analytics_grouped[song.song_id]["date"].append(song.date_of_data)
        else:
            song_detail = Song.query.get(song.song_id)
            song_analytics_grouped[song.song_id] = {
                "id" : song_detail.id,
                "name" : song_detail.name,
                "image" : song_detail.image,
                "play_count" : [song.song_play_count],
                "like_count" : [song.song_like_count],
                "date": [song.date_of_data]
            }

    # group album analytics by album id
    album_analytics_grouped = {}

    for album in album_analytics:
        if(album.album_id in album_analytics_grouped):
            album_analytics_grouped[album.album_id]["play_count"].append(album.album_play_count)
            album_analytics_grouped[album.album_id]["date"].append(album.date_of_data)
        else:
            album_detail = Album.query.get(album.album_id)
            album_analytics_grouped[album.album_id] = {
                "id" : album_detail.id,
                "name" : album_detail.name,
                "image" : album_detail.image,
                "play_count" : [album.album_play_count],
                "date" : [album.date_of_data]
            }
    likes = sum([song.like_count for song in user_songs])
    total_songs = len(user_songs)
    total_albums = len(user_albums)
    play_count = sum([song.play_count for song in user_songs])
    popularity = 2 * user.profile_view_count - (datetime.datetime.now() - user.joined_on).days + play_count + likes + total_songs + total_albums
    return {
        "success" : True,
        "name": user.name,
        "image" : user.image,
        "profile_view_count" : user.profile_view_count,
        "joined_on" : str(user.joined_on.strftime("%B-%Y")),
        "total_songs": total_songs,
        "total_albums": total_albums,
        "total_play_count" : play_count,
        "total_like_count" : likes,
        "total_popularity" : popularity,
        "songs" : song_analytics_grouped,
        "albums" : album_analytics_grouped,
        "Month" : datetime.datetime.now().strftime("%B"),
        "Year" : datetime.datetime.now().strftime("%Y"),
        "MonthYear": datetime.datetime.now().strftime("%B-%Y")
    }


