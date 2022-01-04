from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session           #allow for session creation/maintenance
from flask import redirect
import urllib
import json
import random
from os import urandom
# from jokeapi import Jokes
import asyncio
import db
import sqlite3   #enable control of an sqlite database
import time
app = Flask(__name__)    #create Flask object
app.secret_key = urandom(32) #generates random key

@app.route("/leave",methods=['GET', 'POST'])
def leave_page():
    '''
    Leaves timer page and goes back to the home page when the user presses the "Stop Timer" button
    '''
    # reset all timers
    db.setMinute(session["login"], "None")
    db.setTime(session["login"], "None")
    db.setBreakMinute(session["login"], "None")
    return redirect("/home")

@app.route("/timer",methods=['GET', 'POST'])
def disp_timerpage():
    '''
    Displays the timer/study page
    '''
    if('login' in session and session['login'] != False):
        try:
            db.setMinute(session["login"], checkTime("t"))
            minute = db.getMinute(session["login"])
            print(minute)
            if minute != "None":
                if minute <= 0:
                    db.setMinute(session["login"], "None")
                    db.setTime(session["login"], "None")
                    return redirect("/break")
            else:
                if "timer" in request.form and minute == "None" and int(request.form["timer"]) > 0:
                    db.setMinute(session["login"], int(request.form["timer"]))
                    if(db.getBreakMinute(session["login"]) == "None"):
                        db.setBreakMinute(session["login"], max(1, round(int(db.getMinute(session["login"])) / 3)))
                        print(db.getBreakMinute(session["login"]))
            return render_template('timer.html', minute=db.getMinute(session["login"]))
        except:
            return render_template('login.html', error_message = "ERROR")
        
    return redirect("/")
def checkTime(type):
    if(type == "break"):
        minute = db.getBreakMinute(session["login"])
        if(db.getTime(session["login"]) == "None" or minute == "None"):
            db.setTime(session["login"], time.time()) # initialize start time
        # in break, minute will never equal "None"
        if((time.time() - db.getTime(session["login"])) >= 60): 
            db.setBreakMinute(session["login"], minute - 1)
            db.setTime(session["login"], time.time()) # start time changes every minute
        return db.getBreakMinute(session["login"])
    else:
        minute = db.getMinute(session["login"])
        if(db.getTime(session["login"]) == "None" or minute == "None"):
            db.setTime(session["login"], time.time()) # initialize start time
            return "None"
        if(minute != "None"):
            if((time.time() - db.getTime(session["login"])) >= 60): 
                db.setMinute(session["login"], minute - 1)
                db.setTime(session["login"], time.time()) # start time changes every minute
            return db.getMinute(session["login"])
    
    return "None"
    
@app.route("/break",methods=['GET', 'POST'])
def disp_breakpage():
    '''
    Displays the break page, links the APIs
    '''
    if('login' in session and session['login'] != False):
        try:
            if(db.getBreakMinute(session["login"]) == "None"): #should never equal None, unless the user used the search bar and skipped timer page
                db.setBreakMinute(session["login"], 5)
            db.setBreakMinute(session["login"], checkTime("break"))
            minute = db.getBreakMinute(session["login"])
            if minute != "None":
                if minute <= 0:
                    db.setBreakMinute(session["login"], "None")
                    db.setTime(session["login"], "None")
                    return redirect("/timer")
            response = urllib.request.urlopen("https://asli-fun-fact-api.herokuapp.com/") # join key with base url
            json_stuff = json.loads(response.read())
            data = json_stuff["data"]
            funFact = data["fact"]
            req = urllib.request.Request("http://api.kanye.rest/")
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0')
            response2 = urllib.request.urlopen(req)
            json_stuff2 = json.loads(response2.read())
            print(json_stuff2)
            inspiration = json_stuff2["quote"]
            f = open("keys/key_harvardartmuseums.txt")
            key = f.readline()
            req = urllib.request.Request("https://api.harvardartmuseums.org/image?apikey="+key)
            response2 = urllib.request.urlopen(req)
            json_stuff2 = json.loads(response2.read())
            print(len(json_stuff2["records"]))
            randInt0 = random.randint(0, len(json_stuff2["records"]) - 1)
            randInt1 = random.randint(0, len(json_stuff2["records"]) - 1)
            randInt2 = random.randint(0, len(json_stuff2["records"]) - 1)
            # regenerate integers until they are unique
            while(randInt0 == randInt1 or randInt1 == randInt2 or randInt2 == randInt0):
                randInt0 = random.randint(0, len(json_stuff2["records"]) - 1)
                randInt1 = random.randint(0, len(json_stuff2["records"]) - 1)
                randInt2 = random.randint(0, len(json_stuff2["records"]) - 1)
            images = [json_stuff2["records"][randInt0]["baseimageurl"], json_stuff2["records"][randInt1]["baseimageurl"], json_stuff2["records"][randInt2]["baseimageurl"]]
            print(images)
            return render_template('break.html', name=session["login"], fact = funFact, inspirationQuote=inspiration, images=images, minute=db.getBreakMinute(session["login"]))
        except:
            return render_template('login.html', error_message = "ERROR")
    return redirect("/")

@app.route("/about",methods=['GET','POST'])
def disp_aboutpage():
    '''
    Displays about page
    '''
    return render_template('about.html')

@app.route("/", methods=['GET', 'POST', 'PUT'])
def disp_loginpage():
    '''
    Displays login page and logs users in.
    '''
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request) 
    # print("***DIAG: request.args ***")
    # print(request.args)
    # print("***DIAG: request.args['username']  ***")
    # print(request.args['username']) -- does NOT work - this has not been defined yet - causes error
    print("***DIAG: request.headers ***")
    print(request.headers)

    # checks for request method and gets the input
    data = []
    if(request.method == "GET"):
        data = request.args
    else:
        data = request.form
    if("sub2" in data): # sub2 is added to request.args when the user has logged out, so we can check if it exists to determine whether to end the session or not
        session["login"] = False # end session
    if("login" in session):
        if(session["login"] != False): # if not false, the value of session["login"] is the username of the logged in user
            return redirect("/home") # go straight to home page
    print(session)
    if("username" in data):
        # checks for request method and gets the input
        if(request.method == "GET"):
            name_input = request.args['username']
            pass_input = request.args['password']
        else:
            name_input = request.form['username']
            pass_input = request.form['password']


        error = "" # the error message
        # a try catch block in case anything unexpected happens
        try:
            error = db.get_login(name_input, pass_input)
            if(error == ""):
                session["login"] = name_input
                print("hello")
                return redirect("/home") # auth with spotify
        except Exception as e:
            error = e
        return render_template('login.html', error_message = error) # render login page with an error message
    return render_template('login.html') # otherwise render login page


#@app.route("/auth", methods=['GET', 'POST', 'PUT']) #I temperarily Commented Everything out so at least the page loaded
#def spotify_auth():
    #j = await Jokes()  # Initialise the class
    #await j.get_joke()  # Retrieve a random joke
    #if joke["type"] == "single": # Print the joke
    #    joke01 = (joke["joke"])
    #else:
    #    joke01 = print(joke["setup"])
    #    joke02 = print(joke["delivery"])
    

@app.route("/home", methods=['GET', 'POST', 'PUT']) 
def load_home(): 
    '''
    Loads home page with buttons for timer page and about page
    '''
    if('login' in session and session['login'] != False): # check if user is logged in
        return render_template('home.html', name = session["login"]) # render login page with an error message
    return redirect("/") # if not logged in, go to login page
@app.route("/create_account", methods=['GET', 'POST'])
def create_account_render():
    '''
    Creates a new account for each user
    '''
    # check if input exists by checking if username input is in request dictionary
    if('username' in request.form or 'username' in request.args):
        name_input = "" #username input
        pass_input = "" #password input
        cpass_input = "" #confirm password
        error = "" # error message
        # checks for request method and gets the input
        if(request.method == "GET"):
            name_input = request.args['username']
            pass_input = request.args['password']
            cpass_input = request.args['cpassword']
        else:
            name_input = request.form['username']
            pass_input = request.form['password']
            cpass_input = request.form['cpassword']
        # checks input for validity (it exists, passwords match, etc.)
        if(name_input == ""):
            error = "Username field cannot be blank!"
        elif(pass_input == ""):
            error = "Password field cannot be blank!"
        elif("\\n" in name_input):
            error = "Username cannot contain \\n!"
        elif(pass_input != cpass_input):
            error = "Password fields must match!"
        else:
            try:
                db.add_login(name_input, pass_input) # try to add u/p pair to db
                return redirect("/") # go back to main login page
            except sqlite3.IntegrityError: # will throw this error if the username is a duplicate
                error = "Username already exists!"
        # render the page after processing input
        return render_template('register.html', error_message=error)
    # render the page
    return render_template('register.html')

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
    db.db.close()
