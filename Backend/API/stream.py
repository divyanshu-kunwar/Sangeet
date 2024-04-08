from flask import request, send_file
from flask_restful import Resource
from io import BytesIO

from utility.api import api
from utility.model import audioData
from controller.c_song import increasePlayCount
from utility.cache import cache

@cache.memoize(timeout=3600)
def get_audio(song_id : int):
    print(" Running a query cache miss ")
    audio = audioData.query.filter_by(song_id=song_id).first()
    if(audio):
        return send_file(BytesIO(audio.audio), mimetype='application/octet-stream')


class Stream(Resource):
    def get(self):
        id = request.args.get('id')
        if(id):
            increasePlayCount(id)
            return get_audio(id)
        return {
            "success":True
        }
        
api.add_resource(Stream, '/api/stream')