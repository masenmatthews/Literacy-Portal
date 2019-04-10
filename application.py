import os

from flask import Flask, flash, redirect, session, request, render_template, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tabledef import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return "Hello Boss!"

@app.route("/signup", methods=["POST"])
def signup():
    # Get signup information.
    username = request.form.get("username")
    password = request.form.get("password") 

    # Makes sure that user doesn't already exist
    # if db.execute("SELECT * FROM users WHERE username=username"):
    #     return render_template ("error.html")

    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
               {"username": username, "password": password})
    db.commit()
    return render_template("success.html")

@app.route("/login", methods=["POST"])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
