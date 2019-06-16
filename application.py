import os
import requests
from flask import Flask, flash, redirect, session, request, render_template, abort, url_for, jsonify, json
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from create import *

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

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

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
  
    reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id}).fetchall()
    return render_template("book.html", book=book, reviews=reviews)

@app.route("/review/<int:book_id>", methods=["GET", "POST"])
def review(book_id):
    rating = request.form.get("rating")
    title = request.form.get("title")
    body = request.form.get("body")
    
    db.execute("INSERT INTO reviews (rating, title, body, book_id) VALUES (:rating, :title, :body, :book_id)",
               {"body": body, "book_id": book_id, "rating": rating, "title": title})
    db.commit()    # Add reviewv
    return render_template("success.html")


@app.route("/api/<isbn>", methods=["GET", "POST"])
def book_api(isbn):
    # tricky part is figuring out how to pull book AND isbn here. In other words, how do I get book.title and book.isbn while pulling just the isbn to feed into the get request.
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book.")

    res = requests.get("https://www.goodreads.com/book/review_counts.json", 
        params={"key": "YvzsUe5aIiq75U6rQsp6A", "isbns": book.isbn}).json()
    res = res["books"][0]
    reviews_count = res["reviews_count"]
    average_rating = res["average_rating"]
    data = {
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "reviews_count": reviews_count,
        "average_rating": average_rating
    }
    return json.dumps(data)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=TrÎue, host='0.0.0.0', port=4000)
