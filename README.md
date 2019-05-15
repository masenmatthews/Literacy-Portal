# Project 1

Web Programming with Python and JavaScript

## Setup steps

1. Clone repository to desktop or directory of your choice
2. Navigate to repository using the terminal
3. Run the following commands:
    export FLASK_APP=application.py
    export FLASK_DEBUG=1
    export DATABASE_URL=postgres://nojnxjyrnfsudn:e1caa2c6269e1abdd28e9a7b07fb8813a855656ca98231cece47fb786fba6e13@ec2-54-197-232-203.compute-1.amazonaws.com:5432/d50ghl4mrjj7h
4. Run sudo pip3 install -U -r requirements.txt 
4. Run flask run

https://pythonspot.com/login-authentication-with-flask/
## 

    # Get signup form information.
    # username = request.form.get("username")
    # password = request.form.get("password") 

    # Makes sure that user doesn't already exist
    # if db.execute("SELECT * FROM users WHERE username=username"):
    #     return render_template ("error.html")

    # Add new user to database
    # db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
    #            {"username": username, "password": password})
    # db.commit()

    # if request.form['password'] == 'password' and request.form['username'] == 'admin':
    #     session['logged_in'] = True
    # else:
    #     flash('wrong password!')
    # return index()

https://pythonspot.com/login-authentication-with-flask/