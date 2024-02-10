'''
At the command line, run 

conda activate PIC16B-24W
export FLASK_ENV=development
flask run


# Sources


thius is the one for hw 3

This set of lecture notes is based in part on previous materials developed by [Erin George](https://www.math.ucla.edu/~egeo/) (UCLA Mathematics) and the tutorial [here](https://stackabuse.com/deploying-a-flask-application-to-heroku/). 
'''
from flask import Flask, render_template, request, g
from flask import redirect, url_for, abort
import sqlite3


app = Flask(__name__)

# www.google.com/
@app.route("/") # decorators
def render_base():
    # renders the main page, base.html, which all other pages are built off of
    # base.html gives us the header visible at all times while on the website
    return render_template("base.html")





def get_message_db():
    try:
     # attempt to return the existing message database connection from the global context (g)
     # checks to see if the message_db exists, if it doesnt't it will create one using the except:

        return g.message_db
    except: 
        # creates the database
        g.message_db = sqlite3.connect("message_db.sqlite")
        
        # creates a table messages inside the data base with a handle and message column
        # IF NOT EXISTS means this command will only be ran if the messages table doesnt exist
        cmd = 'CREATE TABLE IF NOT EXISTS messages (handle TEXT, message TEXT)'
        
        # connects to database
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db
    
def insert_message(request):
    # Extract the message and handle from the request
    message = request.form.get("message")
    name = request.form.get("name")
    
    
    # gets database
    database = get_message_db()
    
    # connects to database
    conn = sqlite3.connect('message_db.sqlite')
    
    
    cursor = conn.cursor()
   
    # inserts the message and handle into the messages table

       # creates a function to insert the values into the table
        # the ? represents where the paremeters of name, messages will be passed too
    insert = """
    INSERT INTO messages (handle, message) VALUES (?, ?);
    """
    cursor.execute(insert, (name, message))
    
     # commits the changes and close the connection
    conn.commit()
    conn.close()
        
        # returns the message and name that was submitted
    return message, name


# generates n random mesages
def random_messages(n):
    
    # connects to the database
    conn = sqlite3.connect("message_db.sqlite")
    cursor = conn.cursor()

    # this gets us the total number of messages from the data base
    # this way if n is less than the total number of messages, we won't run into any issues
    cursor.execute("SELECT COUNT(*) FROM messages")
    total = cursor.fetchone()[0]

    # determines the number of messages to retrieve (minimum of n and total_messages)
    minimum = min(n, total)

    # retrieve n random messages from the database
    cursor.execute(f"SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT {minimum}")
    finalmessages = cursor.fetchall()

    # close the cursor and connection
   
    conn.close()

    # returns the gathered messages
    return finalmessages



    # route for the submit page
@app.route("/submit/", methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
         # if the user just visits the url
        return render_template('submit.html')
    else:
        # inserts message into data base
        message, name = insert_message(request)
        
        # render the submit template, thanking the person for their messaage
        return render_template("submit.html",message = message, name = name )    
    
# route for the view page
@app.route("/view/")
def view():
    
    try:
        # if there are messages present, it will show 5 random messages
        msg = random_messages(5)
        return render_template("view.html", messages = msg) 
    except:
        # if no messages are present, it will render and empty view page
         return render_template("view.html") 

    
    


 # route of main page
@app.route("/main/")
def render_main():
    return render_template("main.html")








