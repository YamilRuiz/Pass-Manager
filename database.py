# Yamil Ruiz
# Final Project
# Due Date: 03/03/2023

from mongoengine import *
import os
import random
import bcrypt
from passwordLogic import password_generator
from dotenv import load_dotenv
from mail import mail_sender

load_dotenv()
atlas = os.environ["ATLAS_URI"]
""" Database connection/ ********A Try should be used to test connection*********"""
db = connect(host=atlas)
""" Database name"""
dbCluster = db["test"]
""" Database Collection"""
dbCollection = dbCluster["user"]

class User(Document):

    username = StringField(unique=True, required=True, max_length=25)
    password = StringField(required=True, min_length=8)
    email = EmailField(required=True, unique=True)
    passcode = StringField(max_length=6)
    user_apps = DictField()


"""User Search Function/ Working but error catch not sure"""


# Login function with db check and mail function
def user_login(current_user, password):
    user = dbCollection.find_one({"username": current_user})
    user_password = password.encode("utf-8")
    if bcrypt.checkpw(user_password, user["password"]):
        temp_code = random.randrange(100000, 999999)
        temp_code_add(user["username"], temp_code)
        tempemail = user["email"]
        mail_sender(tempemail, temp_code)
    else:
        raise Exception("Incorrect Password")



# user check at login function
def user_search_login(user):
    user_check = dbCollection.find_one({"username": str(user)})

    if user_check is None:
        return False
    elif user == user_check["username"]:
        return True


# Function for display / Need to beautify output
def user_info(user):
    user_data = dbCollection.find_one({"username": user})
    return user_data


# No use yet for insert collection
def insert_collection(collection):
    dbCollection.insert_one(collection)



# Passcode checker function
def passcode_checker(user, passcode):
    info = dbCollection.find_one({"username": user})
    return_info = info["passcode"]
    if passcode == int(return_info):
        return True
    else:
        return False


# Add temporary code to collection
def temp_code_add(user_query, passcode):
    myquery = {"username": user_query}
    new_values = {"$set": {"passcode": passcode}}
    dbCollection.update_one(myquery, new_values)


# Get user password from app
def document_pull(user):
    info = dbCollection.find_one({"username": user})
    return info


# Function to update apps password
def user_app_update(username, user_app):
    myquery = {"username": username}
    new_password = password_generator()
    app = user_app
    new_values = {"$set": {"user_apps."+app: new_password}}
    dbCollection.update_one(myquery, new_values, upsert=True)


# Will be used to delete single application password
def delete_app_password(username, user_app):
    myquery = {"username": username}
    app = user_app
    dbCollection.update_one(myquery, {'$unset': {"user_apps."+app: ""}})


# Add App to list
def add_app_password(username, user_app):
    myquery = {"username": username}
    password = password_generator()
    app = user_app
    dbCollection.update_one(myquery, {'$set': {"user_apps."+app: password}})

