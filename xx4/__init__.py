from flask import Flask, render_template, request, redirect, url_for, flash, session
import spotify
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/spotifyauth")
def spotifyauth():
    url = spotify.auth_app()
    return redirect(url)

@app.route("/apitest")
def apitest():
    return render_template("test.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
