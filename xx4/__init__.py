from flask import Flask, render_template, request, redirect, url_for, flash, session
import spotify
# from utils import database as db
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def index():
    return render_template("home.html")

'''

@app.route("/createaccount")
def create_account():
	return render_template("createaccount.html")

@app.route("/auth")
def check_creation():
	user = request.args["username"]
	if request.args["password1"] == request.args["password2"]:
		pwd = request.args["password1"]
		unique = make.createAcc(user,pwd)
		if unique:
			flash("Success!")
			return redirect(url_for("hello_world"))
		else:
			flash ("Oops this user already exists")
			return redirect(url_for("create_account"))
	else:
		flash("Passwords do not match :(")
		return redirect(url_for("create_account"))

@app.route("/welcome")
def logged_in():
   input_name = request.args["username"]
   input_pass = request.args["password"]
   hash_object = hashlib.sha224(input_pass)
   hashed_pass = hash_object.hexdigest()
   lookup = db.auth(input_name)
   #Validation process, what went wrong (if anything)?
   if lookup[0]:
	  if hashed_pass == lookup[1][0]:
		 session["username"] = input_name #Creates a new session
		 global username
		 username = input_name
		 return render_template("welcome.html", name = input_name)
	  else:
		 return render_template("login.html", message = "Error: Wrong password")
   else:
	  return render_template("login.html", message =  "Error: Wrong username")
'''

@app.route("/spotifyauth")
def spotifyauth():
    url = spotify.auth_app()
    return redirect(url)

@app.route("/apitest")
def apitest():
    d = spotify.retrieve_token()
    session["access_token"] = d["access_token"]
    # db.update_token(d["refresh_token"])
    print "===========================access token========="
    print session.get('access_token')
    print "===========================access token========="
    return render_template("test.html")

@app.route("/add_track", methods=["POST", 'GET'])
def add_track():
    token = session.get("access_token")
    print "===========================access token========="
    print token
    print "===========================access token========="
    # track = request.form['track'] #need to confirm with html
    #######TESTING###############
    track = "Just the Way You Are"
    track.replace(" ", "%20")
    # artist = request.form['artist'] #need to confirm with html
    artist = "Bruno Mars"
    artist.replace(" ", "%20")
    track_id = spotify.get_track(track, artist, token)
    spotify.add_track(track_id)
    return render_template("test.html", track_id = track_id)

if __name__ == "__main__":
    app.debug = True
    app.run()
