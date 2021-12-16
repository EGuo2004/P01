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

app = Flask(__name__)    #create Flask object
app.secret_key = urandom(32) #generates random key

@app.route("/", methods=['GET', 'POST'])
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
                return redirect("/home") # render welcome page
        except Exception as e:
            error = e
        return render_template('login.html', error_message = error) # render login page with an error message
    return render_template('login.html') # otherwise render login page


@app.route("/home", methods=['GET', 'POST']) #I temperarily Commented Everything out so at least the page loaded
def load_home():
    #j = await Jokes()  # Initialise the class
    #await j.get_joke()  # Retrieve a random joke
    #if joke["type"] == "single": # Print the joke
    #    joke01 = (joke["joke"])
    #else:
    #    joke01 = print(joke["setup"])
    #    joke02 = print(joke["delivery"])
    key = "537460653fc3495991100368458ce398"
    keys = {
         'grant_type': 'client_credentials',
         'client_id': "537460653fc3495991100368458ce398",
         'client_secret': "cb27fce0a98e4d7d9aaccc5d930ba1a8",
    }
    data = urllib.parse.urlencode(keys)
    data = data.encode("ascii")
    response = urllib.request.urlopen("https://accounts.spotify.com/api/token",data=data) # join key with base url
    print(response)
    json_stuff = json.loads(response.read())
    print(json_stuff)
    # headers = {
    #     'Authorization': 'Bearer {token}'.format(token=json_stuff["access_token"])
    # }
    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    # Track ID from the URI
    track_id = '6y0igZArWVi6Iz0rj35c1Y'

    # actual GET request with proper header
    req = urllib.request.Request(BASE_URL + 'audio-features/' + track_id)
    req.add_header('Authorization', 'Bearer {token}'.format(token=json_stuff["access_token"]))
    response = urllib.request.urlopen(req)
    print(json.loads(response.read()))

    response = urllib.request.urlopen("https://asli-fun-fact-api.herokuapp.com/") # join key with base url
    json_stuff = json.loads(response.read())
    data = json_stuff["data"]
    funFact = data["fact"]


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
