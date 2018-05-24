global db
import sqlite3, random
import hashlib

def open_db():
    global db
    f= "../data/spotify.db"
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
    c_dup.execute("CREATE TABLE IF NOT EXISTS rooms(name INTEGER PRIMARY KEY, key TEXT, host_user TEXT, songs TEXT)")

    close()
    return

#Accounts
#==========================================================

#Create an account
#-----------------
def createAcc(user, passw, fname, lname):
    global db
    try:
        open_db()
        c_dup = db.cursor()
        hash_object = hashlib.sha224(passw)
        hashed_pass = hash_object.hexdigest()
        command = "INSERT INTO accounts VALUES(?,?)"
        c_dup.execute(command, (user, hashed_pass))
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
    command = "SELECT username FROM accounts WHERE username = ?"
    c_dup.execute(command, (user))
    users = c_dup.fetchall()
    if len(users) == 0:
        response.append(False)
    else:
        response.append(True)
        command = "SELECT pass FROM accounts WHERE username = ?" 
        c_dup.execute(command,(user))
        pwds = c_dup.fetchall()
        for passw in pwds:
            response.append(passw)
            print passw
    close()
    return response


#==========================================================
#TESTS
#createAcc("jack", "jackpwd")
#createAcc("lils", "lilspwd")
#createBlog("lol", "lel", "dfjaksjd")
#updateBlog(2, "sry fell asleep", "won't happen again")
#print getBlog("lol")
#createBlog("emily", "testing", "does this still work?") #so it does