import csv
import os

from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

metadata = MetaData()
books = Table('books', metadata,
              Column('id', Integer, primary_key=True),
              Column('isbn', String),
              Column('title', String),
              Column('author', String),
              Column('year', String),
              )

books.drop(engine)
books.create(engine)  # creates the users table

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                {"isbn": isbn, "title": title, "author": author, "year": year})
        print(
            f"Added {title} to database")
    db.commit()

if __name__ == "__main__":
    main()
