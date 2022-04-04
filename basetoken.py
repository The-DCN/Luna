from abc import ABC, abstractmethod
from db import db
from authlib.jose.errors import ExpiredTokenError


class BaseToken(ABC):
    
    @abstractmethod
    def create(self):
        pass
    
    @staticmethod
    def validate_token(self, token):
            expired_token = db.collection(u'expired_tokens').document(token).get()
            
            if expired_token.exists:
                raise Exception
            
               
    
    def get_access_token(self):
        return self.access_token
    
    def get_refresh_token(self):
        return self.refresh_token