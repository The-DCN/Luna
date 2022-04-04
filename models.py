import datetime
import json
from abc import ABC, abstractmethod
import time

class User(object):
    def __init__(self, username, password, email,
                 date_of_birth=None, status=None, 
                 city=None, country=None, refresh_token=None,
                 phone_number=None):
        
        self.username = username
        self.password = password
        self.email = email
        self.date_of_birth = date_of_birth
        self.status = status
        self.country = country
        self.city = city
        self.phone_number = phone_number
        self.refresh_token = refresh_token

    def __init__(self, user_dict):
        self.__dict__.update(user_dict)
    
    @staticmethod
    def from_dict(source):
        return json.loads(json.dumps(source), object_hook=User)
    
    def set_refresh_token(self, token):
        self.refresh_token = token
    
    def clear_refresh_token(self):
        self.refresh_token = ''
    
        
    def to_dict(self):
        return self.__dict__

  
class Sleep(object):

    def __init__(self, userid, date, start_time=None, end_time=None, sleep_rating=None, dream_rating=None, sleep_event=None):
        
        self.userid = userid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.sleep_rating = sleep_rating
        self.dream_rating = dream_rating
        self.sleep_event = sleep_event

    def __init__(self, sleep_dict):
        self.__dict__.update(sleep_dict)

    @staticmethod
    def from_dict(source):
        return json.loads(json.dumps(source), object_hook=Sleep)
    
    def to_dict(self):
        return self.__dict__


# class BaseToken(ABC):
    
#     @abstractmethod
#     def create_token():
#         pass
    
#     @abstractmethod
#     @staticmethod
#     def validate_token(token):
#         pass
    
#     @abstractmethod
#     def get_access_token():
#         pass
        
# class JWTToken(BaseToken):
    
#     def __init__(self, username -> str, password -> str, access_token_exp -> int, refresh_token_exp -> int ,  role=[]) -> None:
#         super().__init__()
#         self.username = username
#         self.password = password
#         self.access_token_exp = access_token_exp
#         self.refresh_token_exp = refresh_token_exp
#         self.access_token = None
#         self.refresh_token = None
        
        
#     def create_token(self):
    
#         def is_empty(list):
#             return not list
    
#         current_date = datetime.now()
#         future_date = current_date +  datetime.timedelta(minutes=time)
#         user_role = 'USER'
        
#         #check if the user has a role in the
#         if not is_empty(self.role):
#             user_role = self.role[0]
    
#         header =  {'alg': 'RS256'}
#         payload = {'userid': self.username, 
#                 'iat': str(datetime.now()),
#                 'exp': str(future_date),
#                 'role': user_role}
    
#         token  = jwt.encode(header, payload, key).decode('utf8')
  
#         return token
    
        
    

