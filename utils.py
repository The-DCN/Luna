from __future__ import unicode_literals
from db import db
from models import User
from authlib.jose import jwt
import bcrypt
from datetime import datetime, timedelta
from google.cloud import firestore

'''
METHODS TO BE IMPLEMENTED

create_user():

1. Creating a new user in the database
   - encrypt the password using bcrypt
   - create user object using the provided fields from the request and encrypted the password

2. Getting a user from the database

3. updating a user in the database

4. deleting a user from the database
'''

'''
checks if username exists and valid password
'''
def create_user(first_name,last_name, username, email, password):

        #check if the user already exists 
        user_check = db.collection(u'user').document(username).get()
        
        if user_check.exists:
            raise Exception
        
        #create new user in firestore
        user_ref = db.collection(u'users').document(username)
        
        unicode_pass = bytes(password, "utf8")
        hashed_password = bcrypt.hashpw(unicode_pass, bcrypt.gensalt())
    
        # create dictionary holding data 
        user_data = {
            "first_name" : first_name,
            "last_name" : last_name,
            "username" : username,
            "email" : email,
            "password" : hashed_password
        }
    
        # creating document 
        user_ref.set(user_data)
        
        
    
def validate_user_credentials(username, password):
    
        user_doc_ref = db.collection(u'users').document(username)
        user_doc = user_doc_ref.get()
        
        if user_doc.exists:
            
            user = user_doc.to_dict()
            #convert password to byte array before checking the credentials
            unicode_password = bytes(password, "utf8") 
            return bcrypt.checkpw(unicode_password, user['password'])

        return False 
   

def update_user_credentials(user):
    user_doc_ref = db.collection(u'users').document(
        user.username)
    user_doc_ref.update(user.to_dict())

  


def create_token(username, key, time, role =[]):
    
    def is_empty(list):
        return not list
    
    current_date = datetime.now()
    future_date = current_date +  timedelta(minutes=time)
    user_role = 'USER'
        
    #check if the user has a role in the
    if not is_empty(role):
        user_role = role[0]
    
    header =  {'alg': 'RS256'}
    payload = {'userid': username, 
               'iat': str(datetime.now()),
               'exp': str(future_date),
               'role': user_role}
    
    token  = jwt.encode(header, payload, key).decode('utf8')
  
    return token


def check_refresh_token(token):
    return 'please login again'

'''
this method will add an invalid token into the collection of
banned jwt

uses a utf-8 string of the jwt-token as a document id
expired jwt documents contain:

byte array token
date that
'''
def deactivate_token(token):
    try:
        token_data = {
            'token': bytes(token, 'utf-8'),
            'date_added': firestore.SERVER_TIMESTAMP
        }
        db.collection(u'expired_tokens').document(token).set(token_data)  
    
    except:
        print('something went wrong while trying to add the jwt to the expired tokens')

