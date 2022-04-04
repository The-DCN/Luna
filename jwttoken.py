from datetime import datetime, timedelta
import time
from basetoken import BaseToken
from authlib.jose import jwt
from db import db
from authlib.jose.errors import ExpiredTokenError, DecodeError, BadSignatureError


class JWTToken(BaseToken):
    
    def __init__(self, username, access_token_exp, 
                 refresh_token_exp, key,  role=[]) -> None:
        self.username = username
        self.access_token_exp = access_token_exp
        self.refresh_token_exp = refresh_token_exp
        self.access_token = None
        self.refresh_token = None
        self.key = key
        self.role = role
        
    def create(self):
    
        def is_empty(list):
            return not list
    
        current_date = datetime.now()
        access_token_future_date = current_date + timedelta(minutes=self.access_token_exp)
        refresh_token_future_date = current_date + timedelta(minutes=self.refresh_token_exp)
        key = self.key
        user_role = 'USER'
        
        #check if the user has a role above USER
        if not is_empty(self.role):
            user_role = self.role[0]
            
        header =  {'alg': 'RS256'}
        
        refresh_token_payload = {
            'userid': self.username,
            'iat': str(datetime.now()),
            'exp': str(refresh_token_future_date),
            'role': user_role
            }
        
        access_token_payload = {
            'userid': self.username, 
            'iat': str(datetime.now()),
            'exp': str(access_token_future_date),
            'role': user_role
            }
                
        self.access_token  = jwt.encode(header, access_token_payload, key).decode('utf-8')
        
        self.refresh_token = jwt.encode(header, refresh_token_payload, key).decode('utf-8')
    
    def validate_token(self, token):
        try:
            super.validate_token(token)               
            #decode the token 
            encoded_token = bytes(token, 'utf-8')
            key = open("rsa_public.pem", 'r').read()
            decoded = jwt.decode(encoded_token, key)
            user = decoded['userid']
            user_doc = db.collection(u'users').document(user).get()
            
            if not user_doc.exists:
                deactivate_token(token)
                raise Exception
            
            return user.to_dict()
        
        except DecodeError as e:
            self.deactivate_token(token)
        
        except ExpiredTokenError as  e:
            return self.check_refresh_token()
    
    def check_refresh_token(self, token):
        try:
            key
            refresh_token_decoded = jwt.decode(token, key)
        
        
    def get_access_token(self):
        return super().get_access_token()
    
    def get_refresh_token(self):
        return super().get_refresh_token()
    
    def deactivate_token(self, token):
        try:
            token_data = {
                'token': bytes(token, 'utf-8'),
                'date_added': firestore.SERVER_TIMESTAMP
         }
            db.collection(u'expired_tokens').document(token).set(token_data)  
    
        except Exception as e:
            return e
          
