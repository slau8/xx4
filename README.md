<p align="center"><img src="jimmyjams/static/img/logo.png" width="100px"/></p>

# xx4 presents: JIMMY JAMS

Find our app [here](http://159.89.230.97/)!

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

## Contributors
Shannon Lau, Tiffany Moi, Joyce Wu, Helen Ye

| Name         | Role                         |
| ------------ |------------------------------|
| Shannon (PM) | Front-end                    |
| Tiffany      | Database interaction         |
| Joyce        | Playlist modification        |
| Helen        | Spotify authorization        |
