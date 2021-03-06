'''
This file contains methods that accesses and add to the database.
'''

import sqlite3

#initialize db file
DB_FILE = "database.db"

#connect db
db = sqlite3.connect(DB_FILE)
c = db.cursor()

#create tables for database
command = "CREATE TABLE IF NOT EXISTS "

# Creating table that contains username | password | currentTime | minute, usernames must be unique
c.execute (command + "user_info (username TEXT, password TEXT, currentTime INTEGER, minute INTEGER, breakMinute INTEGER, CONSTRAINT uni_user UNIQUE(username))")


def get_login(username, password):
    """
    Returns the correct error message when the user is logging in.

        Parameters:
            username (str): The username that the user entered
            password (str): The password that the user entered

        Returns:
            "User Not Found": Username does not match any entry in the database
            "Incorrect Password": Username is found in the database but password doesn't match
            "": Username and password matches

    """
    # avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # check if username exists in the db
    command = f"SELECT * FROM user_info WHERE (username = \"{username}\")"
    c.execute(command)
    data = c.fetchall()

    # no user exists
    if(data == []):
        return "User Not Found"

    # password is wrong
    elif(data[0][1] != password):
        return "Incorrect Password"

    # username and password is correct
    else:
        return ""


def add_login(username, password):
    """
    Creates an account in the database
    Adds a new row for new username and password in user_info table in database

        Parameters:
            username (str): The username that the user entered
            password (str): The password that the user entered

        Returns:
            None
    """

    # avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # add username and password pair to database, no stories_contributed blank at account creation
    command = "INSERT INTO user_info VALUES(?, ?, ?, ?, ?)"
    c.execute(command, (username, password, "None", "None", "None"))

    # commit changes to db
    db.commit()

def getTime(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = f"SELECT * FROM user_info WHERE (username = \"{username}\")"
    c.execute(command)
    data = c.fetchall()
    print(data)
    return data[0][2]

def getMinute(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = f"SELECT * FROM user_info WHERE (username = \"{username}\")"
    c.execute(command)
    data = c.fetchall()
    print(data)
    return data[0][3]

def getBreakMinute(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = f"SELECT * FROM user_info WHERE (username = \"{username}\")"
    c.execute(command)
    data = c.fetchall()
    print(data)
    return data[0][4]

def setTime(username, time):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = f"UPDATE user_info SET currentTime=\"{time}\" WHERE (username = \"{username}\")"
    print(command)
    c.execute(command)
    db.commit()
    
def setMinute(username, minute):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = f"UPDATE user_info SET minute=\"{minute}\" WHERE (username = \"{username}\")"
    print(command)
    c.execute(command)
    db.commit()

def setBreakMinute(username, minute):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = f"UPDATE user_info SET breakMinute=\"{minute}\" WHERE (username = \"{username}\")"
    print(command)
    c.execute(command)
    db.commit()