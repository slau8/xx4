global db
import sqlite3, random
import hashlib

def open_db():
    global db
    f= "data/spotify.db"
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
    c_dup.execute("CREATE TABLE IF NOT EXISTS hosts(username TEXT PRIMARY KEY, fname TEXT, lname TEXT, pass TEXT, key TEXT)")
    c_dup.execute("CREATE TABLE IF NOT EXISTS rooms(name TEXT PRIMARY KEY, key TEXT, host_user TEXT, songs TEXT)")

    close()
    return

#Accounts
#==========================================================

#Create an account
#-----------------
def createAcc(user, passw, fname, lname, key = "0000"):
    global db
    try:
        open_db()
        c_dup = db.cursor()
        hash_object = hashlib.sha224(passw)
        hashed_pass = hash_object.hexdigest()
        command = "INSERT INTO hosts VALUES(?,?,?,?,?)"
        c_dup.execute(command, (user, fname, lname, hashed_pass, key))
        
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
    command = command = "SELECT pass FROM hosts WHERE username = \"%s\"" % (user)
    print command
    c_dup.execute(command)
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
#Refresh Acess Tokens

#Rooms
#==========================================================
#Create a room
#-----------------
def createRoom(name, user, key = "0000"):
    try:
        open_db()
        c_dup = db.cursor()
        command = "INSERT INTO rooms VALUES(?,?,?,?)"
        c_dup.execute(command, (name, key, user, ""))
        close()
    except:
        print "Error in Room Creation: Room name already taken."
        return False
    return True

#Add songs
#-----------------

def addSongs(name, key, song):
    try:
        open_db()
        c_dup = db.cursor()
        command = "SELECT songs FROM rooms WHERE name = \"%s\" AND key = \"%s\" " % (name, key)
        c_dup.execute(command)
        songs = c_dup.fetchall()[0][0]
        songs = songs + song + ", "
        command = "UPDATE rooms SET songs =  \"%s\" WHERE name = \"%s\" AND key = \"%s\" " % (songs, name, key)

        c_dup = db.cursor()
        c_dup.execute(command)
        close()
    except:
        print "Wrong Pin or Name"
        return False
    return True

    
#==========================================================
#TESTS
#db_setup()
#createAcc("jack", "Jack", "Boy", "jackpwd")
#createAcc("jack", "lol", "peep", "ksjdlf")
#print auth("jack")
#createRoom("lol", "tim", "0129")
addSongs("lol", "0129", "peep")

