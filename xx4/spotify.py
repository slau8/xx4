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
