import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('postgres://nojnxjyrnfsudn:e1caa2c6269e1abdd28e9a7b07fb8813a855656ca98231cece47fb786fba6e13@ec2-54-197-232-203.compute-1.amazonaws.com:5432/d50ghl4mrjj7h', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("admin", "password")
session.add(user)

user = User("python", "python")
session.add(user)

user = User("jumpiness", "python")
session.add(user)

# commit the record the database
session.commit()
session.commit()
