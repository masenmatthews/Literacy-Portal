import os
from flask import Flask, flash, redirect, session, request, render_template, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

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
        return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    # Get signup information.
    username = request.form.get("username")
    password = request.form.get("password") 
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": username, "password": password})
    db.commit()
    return render_template("success.html")

    # Makes sure that user doesn't already exist
    # if db.execute("SELECT * FROM users WHERE username=username"):
    #     return render_template ("error.html")

    # if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
    #     return render_template("error.html")
    # else:

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

@app.route("/book_search", methods=["POST"])
def book_search():
    book = request.form.get("book")
    books = db.execute("SELECT * FROM books WHERE isbn LIKE :string OR title LIKE :string OR author LIKE :string OR year LIKE :string", {"string": f"%{book}%"}).fetchall()
    return render_template("index.html", books=books)

@app.route("/books/<int:book_id>", methods=("GET", "POST"))
def book(book_id):
    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book.")
        
    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template("book.html", book=book, reviews=reviews)

    # add review
    rating = request.form.get(rating)
    title = request.form.get("title")
    review_body = request.form.get("review_body")
    book.add_review(rating, title, review_body)
    return render_template("success.html")



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=TrÎue, host='0.0.0.0', port=4000)
