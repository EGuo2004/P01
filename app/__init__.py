from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session           #allow for session creation/maintenance
from flask import redirect
import urllib
import json
from os import urandom
# from jokeapi import Jokes
import asyncio
import db
import sqlite3   #enable control of an sqlite database
import time
app = Flask(__name__)    #create Flask object
app.secret_key = urandom(32) #generates random key

minute = None
timeStart = None
@app.route("/timer",methods=['GET', 'POST'])
def disp_timerpage():
    global minute
    minute = checkTime()
    if minute != None:
        if minute <= 0:
            timer = None
            timeStart = None
            return redirect("/break")
    else:
        if "timer" in request.form and minute == None:
            minute = int(request.form["timer"])
    return render_template('timer.html', minute=minute)
def checkTime():
    global minute
    global timeStart
    if(minute != None):
        if((time.time() - timeStart) >= 60): 
            minute -= 1
            timeStart = time.time() # start time changes every minute
        return minute
    if(timeStart == None):
        timeStart = time.time() # initialize start time
        return None
    return None

    

@app.route("/break",methods=['GET', 'POST'])
def disp_breakpage():
	#response2 = urllib.request.urlopen("https://inspiration.goprogram.ai/")
	#json_stuff2 = json.loads(response2.read())
	#inspiration = json_stuff2["quote"]
	#inspirationQuote = inspiration
	return render_template('break.html', name=session["login"])

@app.route("/", methods=['GET', 'POST', 'PUT'])
def disp_loginpage():
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

    response = urllib.request.urlopen("https://asli-fun-fact-api.herokuapp.com/") # join key with base url
    json_stuff = json.loads(response.read())
    data = json_stuff["data"]
    funFact = data["fact"]

    #response2 = urllib.request.urlopen("https://inspiration.goprogram.ai/")
    #json_stuff2 = json.loads(response2.read())
    #inspiration = json_stuff2["quote"]
    


    return render_template('home.html', name = session["login"], fact = funFact) # render login page with an error message

@app.route("/create_account", methods=['GET', 'POST'])
def create_account_render():
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
