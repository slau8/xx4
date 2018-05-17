from flask import Flask, render_template, request, redirect, url_for, flash, session
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello"

if __name__ == "__main__":
    app.debug = True
    app.run()
