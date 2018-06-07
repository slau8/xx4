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
    resp["client_id"] = CLIENT_ID
    # print "=====================ACCOUNT INFO=================="
    # print resp
    # print "=================================================="
    return resp

#gets new token with refresh token
def swap_token(refresh_token):
    url = "https://example.com/v1/refresh"
    authorization_header = {"Content-Type" : "application/x-www-form-urlencoded"}
    params = {"refresh_token": refresh_token}
    req = requests.post(url, data=json.dumps(params), headers=authorization_header)
    resp = json.loads(req.text)
    print resp
    return resp

#get's user's info
def get_user_info(token):
    authorization_header = {"Authorization": "Bearer " + token}
    req = requests.get(USER_PROFILE_URL, headers=authorization_header)
    resp = json.loads(req.text)
    # print ("=============USER INFO================")
    print resp
    # print ("====================================")
    return resp

#gets all of user's playlists
def get_all_playlists(token):
    authorization_header = {"Authorization": "Bearer " + token}
    req = requests.get(USER_PROFILE_URL + '/playlists', headers=authorization_header)
    resp = json.loads(req.text)
    print ("=============USERS PLAYLISTS===========")
    print resp
    print "======================================="
    return resp

# retrieves a lot of possible track_ids
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

# any user may add tracks to playlist
def add_track(track_id, playlist_id, token):
    uri = "spotify:track:" + track_id
    authorization_header = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    params = {"uris": uri}
    user_id = get_user_info(token)['id']
    url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists/' + playlist_id + '/tracks'
    req = requests.post(url, params=params, headers=authorization_header)
    resp = json.loads(req.text)
    print resp
    return resp

#host creates new playlist
def create_playlist(playlist_name, token):
    authorization_header = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    params = {"name": playlist_name}
    user_id = get_user_info(token)['id']
    url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists'
    req = requests.post(url, data=json.dumps(params), headers=authorization_header)
    resp = json.loads(req.text)
    # print "=====================create playlist================="
    # print resp["id"]
    # print "====================================================="
    return resp["id"]

#retrieves song in playlist
def get_playlist(playlist_id, token):
    authorization_header = {"Authorization": "Bearer " + token}
    url = 'https://api.spotify.com/v1/users/' + get_user_info(token)['id'] + '/playlists/' + playlist_id
    req = requests.get(url, headers=authorization_header)
    resp = json.loads(req.text)
    print resp
    return resp

#deletes song in playlist
def delete_track(track_id, playlist_id, token):
    authorization_header = {"Authorization" : "Bearer " + token, "Content-Type": "application/json"}
    user_id = get_user_info(token)['id']
    uri = "spotify:track:" + track_id
    params = {"tracks": [{"uri": uri}]}
    url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists/' + playlist_id + '/tracks'
    method = "delete"
    req = requests.request(method, url, data=json.dumps(params), headers=authorization_header)
    resp = json.loads(req.text)
    print resp
    return resp

################TESTING // ALL FXNS WORKING#############
# get_track('hello', 'BQCWiidi9tIs5TtNoUjZl586elGe8xpZUl7NExVeXTLP2pXmRH2JJypWythgOlDrH1nuK3_0qthCse1P1dLwpfyiAls4vNgVT5RqamldEgyURngrDJXOOEBXj1v5ym-bNBByZQ2Oct15pJ0qL1bXoNKEXBhxhYX0o9nTXJl1Wz2S7Z0')
# add_track('1301WleyT98MSxVHPZCA6M', '7HwlhpxX7ihfhWWrz6ASCf', 'BQCWiidi9tIs5TtNoUjZl586elGe8xpZUl7NExVeXTLP2pXmRH2JJypWythgOlDrH1nuK3_0qthCse1P1dLwpfyiAls4vNgVT5RqamldEgyURngrDJXOOEBXj1v5ym-bNBByZQ2Oct15pJ0qL1bXoNKEXBhxhYX0o9nTXJl1Wz2S7Z0')
# create_playlist("YURRR", 'BQCWiidi9tIs5TtNoUjZl586elGe8xpZUl7NExVeXTLP2pXmRH2JJypWythgOlDrH1nuK3_0qthCse1P1dLwpfyiAls4vNgVT5RqamldEgyURngrDJXOOEBXj1v5ym-bNBByZQ2Oct15pJ0qL1bXoNKEXBhxhYX0o9nTXJl1Wz2S7Z0')
# get_playlist('7HwlhpxX7ihfhWWrz6ASCf', 'BQCWiidi9tIs5TtNoUjZl586elGe8xpZUl7NExVeXTLP2pXmRH2JJypWythgOlDrH1nuK3_0qthCse1P1dLwpfyiAls4vNgVT5RqamldEgyURngrDJXOOEBXj1v5ym-bNBByZQ2Oct15pJ0qL1bXoNKEXBhxhYX0o9nTXJl1Wz2S7Z0')
# get_all_playlists('BQCWiidi9tIs5TtNoUjZl586elGe8xpZUl7NExVeXTLP2pXmRH2JJypWythgOlDrH1nuK3_0qthCse1P1dLwpfyiAls4vNgVT5RqamldEgyURngrDJXOOEBXj1v5ym-bNBByZQ2Oct15pJ0qL1bXoNKEXBhxhYX0o9nTXJl1Wz2S7Z0')
# add_track('1301WleyT98MSxVHPZCA6M', '7HwlhpxX7ihfhWWrz6ASCf', 'BQCWiidi9tIs5TtNoUjZl586elGe8xpZUl7NExVeXTLP2pXmRH2JJypWythgOlDrH1nuK3_0qthCse1P1dLwpfyiAls4vNgVT5RqamldEgyURngrDJXOOEBXj1v5ym-bNBByZQ2Oct15pJ0qL1bXoNKEXBhxhYX0o9nTXJl1Wz2S7Z0')
# delete_track('1301WleyT98MSxVHPZCA6M', '7HwlhpxX7ihfhWWrz6ASCf', 'BQCWiidi9tIs5TtNoUjZl586elGe8xpZUl7NExVeXTLP2pXmRH2JJypWythgOlDrH1nuK3_0qthCse1P1dLwpfyiAls4vNgVT5RqamldEgyURngrDJXOOEBXj1v5ym-bNBByZQ2Oct15pJ0qL1bXoNKEXBhxhYX0o9nTXJl1Wz2S7Z0')
