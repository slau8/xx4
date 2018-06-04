from flask import Flask, render_template, request, redirect, url_for, flash, session
import spotify
from utils import database as db
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/test")
def index():
    return render_template("home.html")

@app.route("/")
def test():
    return render_template("enter.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/create" , methods = ['GET','POST'])
def check_creation():
    user = request.form["username"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    if request.form["password1"] == request.form["password2"]:
        pwd = request.form["password1"]
        unique = db.createAcc(user,pwd, fname, lname)
        if unique:
            flash("Success!")
            return redirect(url_for("spotifyauth"))
        else:
            flash ("Oops this user already exists")
            return redirect(url_for("signup"))
    else:
        flash("Passwords do not match :(")
        return redirect(url_for("signup"))

@app.route("/auth", methods = ['GET','POST'])
def auth():
    input_name = request.form["username"]
    input_pass = request.form["password"]
    hash_object = hashlib.sha224(input_pass)
    hashed_pass = hash_object.hexdigest()
    lookup = db.auth(input_name)
    #Validation process, what went wrong (if anything)?
    if lookup[0]:
        if hashed_pass == lookup[1][0]:
            session["username"] = input_name #Creates a new session
            global username
            username = input_name
            return redirect(url_for("home_logged"))
        else:
            flash("Error: Wrong password")
            return render_template("login.html")
    else:
        flash("Error: Wrong username")
        return render_template("login.html")

@app.route("/profile")
def profile():
    # if 'username' in session:
    # token = session.get('access_token')
        token = 'BQB5VWiFbG8R4hfVzfTalJSRx19M_HXkIFUXEJ6wqEcDKIc8FHI_cvG8eAOWZWxRPg0TuGP7ggG_LD8TCQ6NHO6CcOro2bWovjFE3iffA7VVHELWQA4rx01iLlefxb_M5BaYxhS0K5iIj98r21TA8hGrXrEiLd4JP2KjoLUjOxhOpB4'#session.get("access_token")
        user_info = spotify.get_user_info(token)
        playlists = spotify.get_all_playlists(token)
        return render_template("profile.html", user_info=user_info, playlists=playlists)
    # else:
        # return redirect(url_for('login'))

@app.route("/playlist", methods=["POST", "GET"])
def playlist():
#     if 'username' in session:
# token = session.get('access_token')
        token = 'BQB5VWiFbG8R4hfVzfTalJSRx19M_HXkIFUXEJ6wqEcDKIc8FHI_cvG8eAOWZWxRPg0TuGP7ggG_LD8TCQ6NHO6CcOro2bWovjFE3iffA7VVHELWQA4rx01iLlefxb_M5BaYxhS0K5iIj98r21TA8hGrXrEiLd4JP2KjoLUjOxhOpB4'#session.get("access_token")
        playlist_id = request.args['playlist_id']
        playlist = spotify.get_playlist(playlist_id, token)
        return render_template('playlist.html', playlist=playlist)
#     else:
#         return redirect(url_for('login'))

@app.route("/home_logged")
def home_logged():
    if "username" in session:
        return render_template("home_logged.html")
    else:
        return redirect(url_for("login"))

@app.route("/room_form")
def room_form():
    if "username" in session:
        return render_template("room_form.html")
    else:
        return redirect(url_for("login"))

@app.route("/create_room", methods = ['GET','POST'])
def create_room():
    if "username" in session:
        input_name = request.form["name"]
        input_key = request.form["key"]
        if db.createRoom(input_name, session["username"], input_key):
            flash("Sucess!")
            return redirect(url_for("home_logged"))
        else:
            flash("Room name already taken :(")
            return render_template("room_form.html")
    else:
        return redirect(url_for("login"))


@app.route("/spotifyauth")
def spotifyauth():
    url = spotify.auth_app()
    return redirect(url)

@app.route("/apitest")
def apitest():
    d = spotify.retrieve_token()
    db.addRefresh(d["refresh_token"])
    db.addAccess(d["access_token"])
    print "===========================session token========="
    #print session.get('access_token')
    print "===========================access token========="
    return render_template("test.html")

@app.route("/find_track", methods=["POST", 'GET'])
def find_track():
    token = session.get("access_token")
    try:
        title = request.args["title"]
        title.replace(" ", "%20")
        tracks = spotify.get_track(title, token)
        return render_template("track.html", tracks=tracks)
    except:
        return render_template("search_track.html")

@app.route("/add_track", methods=['POST', 'GET'])
def add_track():
    token = session.get("access_token")
    try:
        track_id = request.form('track_id')
        spotify.add_track(track_id, token)
        flash('Successfully added!')
        return redirect(url_for('test'))
    except:
        flash('We could not add the song. Try again.')
        return redirect(url_for('find_track'))


if __name__ == "__main__":
    app.debug = True
    app.run()
