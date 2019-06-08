# Literary Portal

A one stop shop for all of your online literary needs!

## Live preview

This application is almost complete! A live preview will be added when Goodreads API functionality is added.

## Description

## Technologies
This application utilizes the following technologies:

-Python
-Flask
-SQL
-SQLAlchemy

## Setting up a database

## Setup steps

1. Clone repository to desktop or directory of your choice
2. Navigate to repository using the terminal
3. Run the following commands (in this order):
    export FLASK_APP=application.py

    export FLASK_DEBUG=1

    export DATABASE_URL=[YOUR DATABASE URL HERE]

    sudo pip3 install -U -r requirements.txt 

    python create.py

    python import.py

4. Run flask run