global db
import sqlite3, random
import os
import hashlib

def open_db():
    global db
    path = os.path.dirname(os.path.realpath(__file__))
    f= os.path.join(path, '../data/spotify.db')
    db = sqlite3.connect(f, check_same_thread = False) #open if f exists, otherwise create
    return

def close():
    global db
    db.commit() #save changes
    db.close()  #close database
    return

def db_setup():
    global db
    open_db()
    c_dup = db.cursor()
    c_dup.execute("CREATE TABLE IF NOT EXISTS hosts(username TEXT PRIMARY KEY, fname TEXT, lname TEXT, pass TEXT, access_key TEXT, refresh_token TEXT)")
    c_dup.execute("CREATE TABLE IF NOT EXISTS rooms(name TEXT PRIMARY KEY, key TEXT, host_user TEXT, songs TEXT, playlist_id TEXT)")

    close()
    return

#Accounts
#==========================================================

#Create an account
#-----------------
def createAcc(user, passw, fname, lname, key = "0000", token = "0000"):
    global db
    try:
        open_db()
        c_dup = db.cursor()
        hash_object = hashlib.sha224(passw)
        hashed_pass = hash_object.hexdigest()
        command = "INSERT INTO hosts VALUES(?,?,?,?,?,?)"
        c_dup.execute(command, (user, fname, lname, hashed_pass, key, token))
        close()
    except:
        print "Error in Account Creation: Username already taken."
        return False
    return True
#==========================================================

#For authentication stuff
#returns list of [user_exists, passw]
def auth(user):
    response = []
    open_db()
    c_dup = db.cursor()
    command = "SELECT pass FROM hosts WHERE username = ?"
    print command
    c_dup.execute(command, (user,))
    pwds = c_dup.fetchall()
    if len(pwds) == 0:
        response.append(False)
    else:
        response.append(True)
        for passw in pwds:
            response.append(passw)
            print passw
    close()
    return response

#==========================================================
#Refresh Tokens

def addAccess(user, token):
    open_db()
    c_dup = db.cursor()
    command = "UPDATE hosts SET access_key =  ? WHERE username = ?"
    print command
    c_dup.execute(command,  (token, user,))
    close()

def addRefresh(user, token):
    open_db()
    c_dup = db.cursor()
    command = "UPDATE hosts SET refresh_token =  ? WHERE username = ?"
    c_dup.execute(command, (token, user,))
    close()

def getAccess(user):
    open_db()
    c_dup = db.cursor()
    command = "SELECT access_key FROM hosts WHERE username = ?"
    c_dup.execute(command, (user,))
    token = c_dup.fetchall()[0][0]
    close()
    return token

def getRefresh(user):
    open_db()
    c_dup = db.cursor()
    command = "SELECT refresh_token FROM hosts WHERE username = ?"
    c_dup.execute(command, (user,))
    token = c_dup.fetchall()[0][0]
    close()
    return token

#Rooms
#==========================================================
#Create a room
#-----------------
def createRoom(name, user, key, playlist_id):
    try:
        open_db()
        c_dup = db.cursor()
        command = "INSERT INTO rooms VALUES(?,?,?,?,?)"
        c_dup.execute(command, (name, key, user, "", playlist_id))
        close()
    except:
        print "Error in Room Creation: Room name already taken."
        return False
    return True

#Access a room
#-----------------
def accessRoom(name, key):
    try:
        open_db()
        c_dup = db.cursor()
        command = "SELECT name FROM rooms WHERE name = ? AND key = ?"
        c_dup.execute(command, (name, key,))
        close()
    except:
        print "Wrong name or key"
        return False
    return True

#Get host's rooms
#-----------------
def getRooms(username):
    try:
        open_db()
        c_dup = db.cursor()
        command = "SELECT playlist_id FROM rooms WHERE host_user = ?"
        c_dup.execute(command, (username, ))
        rooms = c_dup.fetchall()
        close()
    except:
        print "Wrong host username"
        return ""
    print "===================ROOMS===================="
    print rooms
    print "============================================"
    return rooms

#Add songs
#-----------------

def addSongs(name, song):
    try:
        open_db()
        c_dup = db.cursor()
        command = "SELECT songs FROM rooms WHERE name = ?"
        c_dup.execute(command, (name, ))
        print name
        print song
        songs = c_dup.fetchall()[0][0]
        songs = songs + song + ", "
        print songs
        command = "UPDATE rooms SET songs =  ? WHERE name = ?"
        c_dup = db.cursor()
        c_dup.execute(command, (songs, name,))
        close()
    except:
        print "Wrong Name"
        return False
    return True

#Get songs
#-----------------

def getSongs(name):
    try:
        open_db()
        c_dup = db.cursor()
        command = "SELECT songs FROM rooms WHERE name = ?"
        c_dup.execute(command, (name, ))
        songs = c_dup.fetchall()[0][0]
        close()
    except:
        print "Wrong Name"
        return ""
    return songs

#Get token
#-----------------

def getToken(name):
    try:
        open_db()
        c_dup = db.cursor()
        command = "SELECT host_user FROM rooms WHERE name = ?"
        c_dup.execute(command, (name, ))
        user = c_dup.fetchall()[0][0]
        close()

        key = getAccess(user)

    except:
        print "Wrong Name"
        return ""
    return key



#==========================================================
#TESTS
#db_setup()
#createAcc("jack", "Jack", "Boy", "jackpwd")
#createAcc("jack", "lol", "peep", "ksjdlf")
#auth("jack")
#createRoom("lol", "tim", "0129")
#addSongs("jeez", "peep")
# addAccess("lol", "djsafkjl")
