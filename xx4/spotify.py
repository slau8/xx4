import requests
import urllib

CLIENTSIDE_URL = 'http://127.0.0.1:5000'
CLIENT_ID = ''
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
