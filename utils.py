from db import db
import bcrypt
from models import User
from authlib.jose import jwt
import functools
from datetime import datetime, timedelta
from google.cloud import firestore

'''
METHODS TO BE IMPLEMENTED

create_user():

1. Creating a new user in the database
- encrypt the password using bcrypt
- create user object using the provided fields from the request and encrypted the password
-  

update_user():
2. updating a user in the database


3. deleting a user from the database

4. getting an individual user from the database
    
'''

'''
checks if username exists and valid password
'''
        
        

def validate_user_credentials(username, password):
    try:
        user_doc_ref = db.collection(u'users').document(username)
        user_doc = user_doc_ref.get()
    
        if user_doc.exists:
            user = User.from_dict(user_doc.to_dict())
            return user.password == password

        return False 
    
    except Exception as e:
        return None
   

def update_user_credentials(user):
    user_doc_ref = db.collection(u'users').document(
        user.username)
    user_doc_ref.update(user.to_dict())
    
    
def create_access_token(username, key, role =[]):
    
    current_date = datetime.now()
    future_date = current_date +  timedelta(hours=1)
    header =  {'alg': 'HS256'}
    payload = {'userid': username, 
               'iat': str(datetime.now()),
               'exp': str(future_date),
               'role': 'USER'}
    token  = jwt.encode(header, payload, key)
  
    return token.decode('utf8')

def create_refresh_token(username, key):

    header = {'alg': 'HS256'}
    
    current_date = datetime.now()
    future_date = current_date +  timedelta(hours=48)
    payload = {'iat':str(current_date), 
               'exp':str(future_date),
               }
    
    token = jwt.encode(header, payload, key)
    return token.decode('utf8')


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
