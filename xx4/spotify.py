import requests
import urllib

CLIENTSIDE_URL = '127.0.0.1:5000'
CLIENT_ID = '873ca57519784131a2bbb3517d77a6d7'
AUTH_URL = 'https://accounts.spotify.com/authorize/?'
REDIRECT_URI = CLIENTSIDE_URL + '/apitest'
SCOPE = 'playlist-modify-public'

def auth_app():
    auth_params = {
            # TODO: Look into using state for security
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'scope': SCOPE
        }
    url = AUTH_URL + urllib.urlencode(auth_params)
    print url
    return url
