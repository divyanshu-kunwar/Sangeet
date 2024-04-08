from flask import request
from flask_restful import Resource
from utility.api import api

from controller.c_song import searchSong
from controller.c_album import searchAlbums
from controller.c_user import SearchArtist

class Search(Resource):
    def get(self):
        query = request.args.get('q')
        # search for artist albums and songs
        # whichever return success with non empty array return that
        artists = SearchArtist(query)
        albums = searchAlbums(query)
        songs = searchSong(query)
        data = {
            "success": True,
        }
        if(artists['success']):
            data['artists'] = artists['data']
        if(albums['success']):
            data['albums'] = albums['data']
        if(songs['success']):
            data['songs'] = songs['data']
        return data

api.add_resource(Search, '/api/search')