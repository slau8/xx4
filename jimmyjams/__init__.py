from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils import spotify
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

@app.route("/enter", methods = ['GET','POST'])
def enter():
    name = request.form["name"].strip()
    if name.find(",") > -1 or name.find(";") > -1:
        flash('Invalid Characters in Name (No "," or ";")')
        return redirect(url_for("test"))

    room_name = request.form["room_name"].strip()
    key = request.form["key"].strip()

    if db.accessRoom(room_name, key):
        session["name"] = name
        session['room'] = room_name
        return redirect(url_for("room"))
    else:
        flash('Wrong room name or key')
        return redirect(url_for("test"))

@app.route("/room")
def room():
    if 'room' in session:
        songs = db.getSongs(session.get("room")).split(",")
        song_list = []
        for each in songs:
            song_list.append(each.split(";"))
        return render_template("room.html", song_list = song_list)
    else:
        flash("Sign Into A Room First!")
        return redirect(url_for("test"))

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
            session['username'] = user
            print 'asdfjasdjfsdjf<><>' + user
            print '***' + session['username']
            flash("Welcome! Login here.")
            return redirect(url_for("spotifyauth"))
        else:
            flash ("Sorry, this username already exists. Try again.")
            return redirect(url_for("signup"))
    else:
        flash("Passwords do not match. Try again.")
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
            return redirect(url_for("home_logged"))
        else:
            flash("Error: Incorrect password.")
            return render_template("login.html")
    else:
        flash("Error: Incorrect username.")
        return render_template("login.html")

#displays songs in each playlist
@app.route("/playlist", methods=["POST", "GET"])
def playlist():
    if 'username' in session:
        token = db.getAccess(session.get("username"))
        playlist_id = request.args['playlist_id']
        playlist = spotify.get_playlist(playlist_id, token)
        return render_template('playlist.html', playlist=playlist)
    else:
        return redirect(url_for('login'))

@app.route("/home_logged")
def home_logged():
    if "username" in session:
        token = db.getAccess(session.get("username"))
        user = spotify.get_user_info(token)
        playlist_ids = db.getRooms(session.get("username"))
        print "=======playlist ids========"
        print playlist_ids
        print "==========================="
        token = db.getAccess(session.get("username"))
        rooms = spotify.get_playlists(playlist_ids, token)
        return render_template("home_logged.html", rooms=rooms, user=user)
    else:
        return redirect(url_for("login"))

@app.route("/room_form")
def room_form():
    if "username" in session:
        return render_template("room_form.html")
    else:
        flash("Please Login First")
        return render_template("login.html")

@app.route("/create_room", methods = ['GET','POST'])
def create_room():
    if "username" in session:
        input_name = request.form["name"]
        input_key = request.form["key"]
        token = db.getAccess(session.get("username"))
        #need to create column for playlist id
        playlist_id = spotify.create_playlist(input_name, token)
        if db.createRoom(input_name, session["username"], input_key, playlist_id):
            flash("Success!")
            return redirect(url_for("home_logged"))
        else:
            flash("Room name already taken :(")
            return render_template("room_form.html")
    else:
        return redirect(url_for("login"))

@app.route("/spotifyauth")
def spotifyauth():
    if "username" in session:
        url = spotify.auth_app()
        global username
        username = session.get("username")
        print "SPOTIFY AUTH " + username
        return redirect(url)
    else:
        flash("Please Login First")
        return render_template("login.html")

@app.route("/apitest")
def apitest():
    d = spotify.retrieve_token()
    if username != "":
        session["username"] = username
        db.addRefresh(session.get("username"), d["refresh_token"])
        db.addAccess(session.get("username"), d["access_token"])
        print "===========================access token========="
        print session.get('access_token')
        print "================================================"
        return redirect(url_for("home_logged"))
    else:
        flash("Please Login First")
        return render_template("login.html")

@app.route("/find_track", methods=["POST", 'GET'])
def find_track():
    if "room" in session:
        token = db.getToken(session.get("room"))
        try:
            title = request.form["song_name"]
            title.replace(" ", "%20")
            tracks = spotify.get_track(title, token)
            return render_template("track_results.html", tracks = tracks)
        except:
            print "error"
            return render_template("search_track.html")
    else:
        flash("Sign Into A Room First!")
        return redirect(url_for("test"))


@app.route("/add_track", methods=['POST', 'GET'])
def add_track():
    if "room" in session:
        token = db.getToken(session.get("room"))
        try:
            #wont print out full name?
            track_name = request.form['track_name']
            track_artist = request.form['track_artist']
            track_id = request.form['track_id']
            user = session.get("name")
            room_name = session.get("room")
            insert = track_name + ";" + track_artist + ";" + user
            db.addSongs(room_name, insert)

            #Not sure why this isnt working
            spotify.add_track(track_id, token)
            flash('Successfully added!')
            return redirect(url_for('test'))
        except:
            flash('We could not add the song. Try again.')
            return redirect(url_for('find_track'))
    else:
        flash("Sign Into A Room First!")
        return redirect(url_for("test"))



if __name__ == "__main__":
    app.debug = True
    app.run()
