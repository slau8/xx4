from flask import request
import requests
import urllib
import base64
import json

with open('.api', 'rU') as f:
    CLIENT_INFO = json.loads(f.read())

CLIENT_ID = CLIENT_INFO['client_id']
CLIENT_SECRET = CLIENT_INFO['client_secret']

CLIENTSIDE_URL = 'http://127.0.0.1:5000'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = CLIENTSIDE_URL + '/apitest'
SCOPE =  'playlist-modify-public'
CREATE_PLAYLIST_URL = 'https://api.spotify.com/v1/users/' + CLIENT_ID + '/playlists'
USER_PROFILE_URL = 'https://api.spotify.com/v1/me'
API_URL = 'https://api.spotify.com'

def auth_app():
    auth_params = {
            # TODO: Look into using state for security
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'scope': SCOPE
        }
    url = AUTH_URL + "/?" + urllib.urlencode(auth_params)
    print url
    return url

def retrieve_token():
    print request.args
    try:
        token = request.args['code']
    except:
        try:
            error = request.args['error']
            return error
        except:
            print("Fail")
            return None
    token_params = {
        "grant_type": "authorization_code",
        "code": str(token),
        "redirect_uri": REDIRECT_URI
    }
    encoded = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
    headers = {
            "Authorization": "Basic " + encoded
    }
    req = requests.post(TOKEN_URL, data=token_params, headers=headers)

    resp = json.loads(req.text)
    return resp

def get_track(track, token):
    params = {"q": track, "type": "track"}
    authorization_header = {"Authorization": "Bearer " + token}
    req = requests.get(API_URL + "/v1/search", params=params, headers=authorization_header)
    resp = json.loads(req.text)
    # print "======================TRACK ID==============="
    #print resp
    # print "============================================="
    results = resp["tracks"]["items"]
    #print results
    tracks = []
    for result in results:
        track_name = result['album']['name']
        track_artist = result['album']['artists'][0]['name']
        track_id = result["uri"].split(":")[2]
        tracks.append([track_name, track_artist, track_id])
    print tracks
    return tracks

def add_track(track_id, token):
    authorization_header = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    params = {"name": "test"}
    req = requests.post('https://api.spotify.com/v1/users/' + CLIENT_ID + '/playlists', params=params, headers=authorization_header)
    resp = json.loads(req.text)
    print resp
    return resp
