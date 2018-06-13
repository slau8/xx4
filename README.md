<p align="center"><img src="jimmyjams/static/img/logo.png" width="100px"/></p>

# xx4 presents: JIMMY JAMS

Find our app [here](http://159.89.230.97/)!

Watch a demo [here](https://www.youtube.com/watch?9=&v=YgQWEBAO9NE)!

Jimmy Jams is a web application that allows people to request music in real time. Hosts of a party can create a “music room” with a corresponding name and key. After inputting the music room credentials, a user can enter the room and input a song, which is added to the playlist queue via the Spotify API. The host of the room will receive a hyperlink to the Spotify playlist, playable from any device.

## How It Works
*Jimmy would like to take music requests at his party. Here's how he will do it with Jimmy Jams.*
1. Jimmy creates an account and links it to his Spotify account.
2. Jimmy sets up a room by creating a room name and key. These credentials are personally distributed to his friends at the party.
3. Jimmy's friends request songs via the app's search feature, which are saved in the SQLite3 database.
4. Jimmy's account will auto-refresh to retrieve songs from the database and push them onto Jimmy's playlist.
5. Jimmy can visit the collaborative playlist on the app or on Spotify.

## Dependencies
* Python 2.7
* Flask
* SQLite3
* HTML/CSS

## Running the App (Locally)
### Virtual Environment and Flask
Flask needs to be installed in order to run this program locally. It is ideally stored in a virtual environment (venv).

To install a venv called `<name>`, run these commands in your terminal:
```
$ pip install virtualenv
$ virtualenv <name>
```
On Mac/Linux, start up your venv with:
```
$ . <name>/bin/activate
```
On Windows:
```
$ . <name>/Scripts/activate
```
In your activated venv, run the following:
```
$ pip install flask
```

### SQLite3
Download SQLite3 [here](https://www.sqlite.org/download.html).

### API Configuration
This app utilizes the Spotify API and requires credentials from the app.

For your [Spotify](https://developer.spotify.com/dashboard/) API credentials:
1. After logging in, click *Create a Client ID* in the upper-right corner.
2. Enter app name, type, and description (Jimmy Jams, website, app that receives music requests and curates a Spotify playlist).
3. In app settings, add `http://127.0.0.1:5000/apitest` as a redirect URI.
3. Your Client ID and Client Secret will appear on your dashboard.

Clone the repo and move into the utils directory:
```
$ git clone git@github.com:slau8/xx4.git
$ cd xx4/jimmyjams/utils
```
Create ``` .api ``` and add your credentials in their appropriate location. For example:
```
{
  "client_id": "this_is_your_client_id",
  "client_secret": "this_is_your_client_secret"
}
```

### Go!
With your virtual environment activated, run:
```
$ cd ..
$ python __init__.py
```
You can now view the webpage by opening the URL `localhost:5000` in Chrome, Firefox, or Safari.

## Contributors
Shannon Lau, Tiffany Moi, Joyce Wu, Helen Ye

| Name         | Role                         |
| ------------ |------------------------------|
| Shannon (PM) | Front-end                    |
| Tiffany      | Database interaction         |
| Joyce        | Playlist modification        |
| Helen        | Spotify authorization        |
