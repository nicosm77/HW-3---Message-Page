'''
At the command line, run 

conda activate PIC16B-24W
export FLASK_ENV=development
flask run

# Sources

This set of lecture notes is based in part on previous materials developed by [Erin George](https://www.math.ucla.edu/~egeo/) (UCLA Mathematics) and the tutorial [here](https://stackabuse.com/deploying-a-flask-application-to-heroku/). 
'''
from flask import Flask, render_template, request
from flask import redirect, url_for, abort

app = Flask(__name__)

# www.google.com/
@app.route("/") # decorators
def hello_world():
    return "<h1>Hello, World!</h1>"

# www.google.com/cat/
@app.route("/hp/")
def marauders():
    return "<p>I solemnly swear I am up to no good.</p>" # p is for paragraph

@app.route("/main/")
def render_main():
    return render_template("main.html")
    # use html templates to avoid writing out looong python strings

@app.route("/move/")
def move():
    return redirect(url_for('login')) 
    # don't do anything else, just redirect user to login page immediately

@app.route('/login/')
def login():
    # immediately abort
    abort(401) # this is the HTTP status code


@app.route("/ask/", methods=['POST', 'GET'])
def ask():
    if request.method == 'GET':
        # if the user just visits the url
        return render_template('ask.html')
    else:
        # if the user submits the form
        name = request.form['name']
        student = request.form['student']
        return render_template('ask.html', name=name, student=student)

@app.route("/profile/<name>")
def hello_name(name):
    return render_template('profile.html', name=name)
