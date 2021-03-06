from flask import Flask, render_template, request, redirect, url_for, flash, session
from jimmyjams.utils import spotify
from jimmyjams.utils import database as db
#from utils import spotify
#from utils import database as db
import hashlib
import os, json
global username

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route("/", methods = ['GET','POST'])
def test():
    if "mode" in session:
        if session["mode"] == "host":
            return redirect(url_for("home_logged"))
        return render_template("enter.html", logged_in = logged_in())
    else:
        return render_template("enter.html", logged_in = logged_in())

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
        session["mode"] = "collaborator"
        return redirect(url_for("room"))
    else:
        flash('Wrong room name or key')
        return redirect(url_for("test"))

@app.route("/room", methods = ['GET','POST'])
def room():
    try: 
        room = request.form["room"]
        session['room'] = room
    except:
        pass

    if 'room' in session:
        room = session.get("room")
        p_id = db.getPlaylistid(room)
        try:
            token = db.getToken(session.get("room"))
            playlist = spotify.get_playlist(p_id, token)
        except:
            host = db.getHost(session.get("room"))
            refresh = db.getRefresh(host)
            token = spotify.swap_token(refresh)["access_token"]

            db.addAccess(host, token)
            playlist = spotify.get_playlist(p_id, token)

        link = playlist['external_urls']['spotify']
        songs = db.getSongs(session.get("room")).split(",")
        song_list = []
        room_name = session.get("room")

        for each in songs:
            if each.strip() != "":
                song_list.append(each.split(";"))

        try:
            if request.form["host"] == "host":
                session["mode"] = "host"
        except:
            session["mode"] = "collaborator"

        if session["mode"] == "collaborator":
            mode = True
        else:
            mode = False

        return render_template("room.html", song_list = song_list, room_name=room_name, link = link, logged_in = logged_in(), is_collaborator = mode)

    else:
        flash("Sign Into A Room First!")
        return redirect(url_for("test"))

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if "username" in session:
        flash("You're already logged in!")
        return redirect(url_for("home_logged"))
    else:
        return render_template("signup.html", logged_in = False)

@app.route("/login", methods = ['GET','POST'])
def login():
    if "username" in session:
        flash("You're already logged in!")
        return redirect(url_for("home_logged"))
    else:
        return render_template("login.html", logged_in = False)

@app.route("/logout", methods = ['GET','POST'])
def logout():
    if "username" in session:
        session.pop("username")
        flash('Successfully logged out.')
        return redirect(url_for("test"))
    else:
        return redirect(url_for("test")) 

@app.route("/host", methods = ['GET','POST'])
def host():
    session["mode"] = "host"
    return redirect(url_for("home_logged"))

@app.route("/collaborator", methods = ['GET','POST'])
def collaborator():
    session["mode"] = "collaborator"
    return redirect(url_for("test"))

@app.route("/create" , methods = ['GET','POST'])
def check_creation():
    if "username" in session:
        flash("You're already logged in!")
        return redirect(url_for("home_logged"))
    else:
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
                flash("Welcome!")
                return redirect(url_for("spotifyauth"))
            else:
                flash ("Sorry, this username already exists. Try again.")
                return redirect(url_for("signup"))
        else:
            flash("Passwords do not match. Try again.")
            return redirect(url_for("signup"))

@app.route("/auth", methods = ['GET','POST'])
def auth():
    if "username" in session:
        flash("You're already logged in!")
        return redirect(url_for("home_logged"))
    else:
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
                return render_template("login.html", logged_in = False)
        else:
            flash("Error: Incorrect username.")
            return render_template("login.html", logged_in = False)

@app.route("/playlist_info", methods = ['GET','POST'])
def playlist_info():
    if 'room' in session:
        songs = db.getSongs(session.get("room")).split(";;")
        song_list = []
        room = session.get("room")
        for each in songs:
            each = each.replace("%30", ",")
            if each.strip() != "":
                song_list.append(each.split(";"))
    response = { "songs" : song_list}
    print response
    return json.dumps(response)

@app.route("/home_logged", methods = ['GET','POST'])
def home_logged():
    if "username" in session:
        try:
            token = db.getAccess(session.get("username"))
            rooms = spotify.get_playlists(playlist_ids, token)
        except:
            refresh = db.getRefresh(session.get("username"))
            token = spotify.swap_token(refresh)["access_token"]
            username = session["username"]
            db.addAccess(username, token)

        user = spotify.get_user_info(token)
        playlist_ids = db.getRooms(session.get("username"))
        rooms = spotify.get_playlists(playlist_ids, token)
        print "=======playlist ids========"
        print playlist_ids
        print "==========================="
        name = db.getName(session.get("username"))
        print name

        return render_template("home_logged.html", name=name, rooms=rooms, user=user, logged_in = True)
    else:
        return redirect(url_for("login"))

@app.route("/room_form")
def room_form():
    if "username" in session:
        return render_template("room_form.html", logged_in = True)
    else:
        flash("Please Login First")
        return render_template("login.html", logged_in = False)

@app.route("/create_room", methods = ['GET','POST'])
def create_room():
    if "username" in session:
        input_name = request.form["name"]
        input_key = request.form["key"]

        try:
            token = db.getAccess(session.get("username"))
            playlist_id = spotify.create_playlist(input_name, token)
        except:
            refresh = db.getRefresh(session.get("username"))
            token = spotify.swap_token(refresh)["access_token"]
            username = session["username"]
            db.addAccess(username, token)
            playlist_id = spotify.create_playlist(input_name, token)

        if db.createRoom(input_name, session["username"], input_key, playlist_id):
            flash("Success!")
            return redirect(url_for("home_logged"))
        else:
            flash("Room name already taken :(")
            return render_template("room_form.html", logged_in = True)
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
        return render_template("login.html", logged_in = False)

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
        return render_template("login.html", logged_in = False)
'''
@app.route("/search")
def search():
    if "room" in session:
        return render_template("search_track.html")
    else:
        flash("Sign Into A Room First!")
        return redirect(url_for("test"))
'''
@app.route("/find_track", methods=["POST", 'GET'])
def find_track():
    if "room" in session:
        token = db.getToken(session.get("room"))
        title = request.form["song_name"]
        title.replace(" ", "%20")
        try:
            tracks = spotify.get_track(title, token)
        except:
            host = db.getHost(session["room"])
            refresh = db.getRefresh(host)
            token = spotify.swap_token(refresh)["access_token"]
            db.addAccess(host,token)
            tracks = spotify.get_track(title, token)
        if "username" in session:
            return render_template("track_results.html", tracks = tracks, logged_in = True)
        else:
            return render_template("track_results.html", tracks = tracks, logged_in = False)
    else:
        flash("Sign Into A Room First!")
        return redirect(url_for("test"))

@app.route("/add_track", methods=['POST', 'GET'])
def add_track():
    if "room" in session:
        token = db.getToken(session.get("room"))
        print "TOKEN ====== " + token
        try:
            track_name = request.form['track_name']
            track_name = track_name.replace("%20", " ")
            track_name = track_name.replace(",", "%30")


            track_artist = request.form['track_artist']
            track_artist = track_artist.replace("%20", " ")

            track_id = request.form['track_id']
            try: 
                user = session.get("name")
            except:
                user = session.get("username") + " (host)"
            room_name = session.get("room")
            insert = track_name + ";" + track_artist + ";" + user + ";" + track_id
            db.addSongs(room_name, insert)
            print "Cool"

            p_id = db.getPlaylistid(room_name)
            print "P_ID" + p_id

            spotify.add_track(track_id, p_id, token)
            flash('Successfully added!')
            return redirect(url_for('room'))
        except:
            flash('We could not add the song. Try again.')
            return redirect(url_for('find_track'))
    else:
        flash("Sign Into A Room First!")
        return redirect(url_for("test"))

@app.route("/remove_track", methods=["POST"])
def remove_track():
    if request.method == "POST":
        try:
            artist = request.form['artist']
            song = request.form['song']
            track = request.form['id']
            attempt = False
            try:
                p_id = db.getPlaylistid(session.get("room"))
                token = db.getToken(session.get("room"))
                resp = spotify.delete_track(track, p_id, token)
                print resp
                attempt = True
            except:
                print "Something went wrong...?"
            attempt = db.removeSongs(session.get("room"), song, artist)
            if attempt:
                flash("Removed song")
            else:
                flash("Could not remove song")
        except:
            print "==============="
            print request.form
            flash("Failed to remove song")
    return redirect(url_for("room"))

def logged_in():
    if "username" in session:
        return True
    return False

if __name__ == "__main__":
    app.debug = True
    app.run()
