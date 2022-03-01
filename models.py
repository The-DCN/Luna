import json


class User(object):
    def __init__(self, username, password, email,
                 date_of_birth=None, status=None, 
                 city=None, country=None, refresh_token=None,
                 phone_number=None, is_active=False):
        
        self.username = username
        self.password = password
        self.email = email
        self.date_of_birth = date_of_birth
        self.status = status
        self.country = country
        self.city = city
        self.phone_number = phone_number
        self.refresh_token = refresh_token
        self.is_active = is_active

    def __init__(self, user_dict):
        self.__dict__.update(user_dict)
    
    @staticmethod
    def from_dict(source):
        return json.loads(json.dumps(source), object_hook=User)
    
    def set_refresh_token(self, token):
        self.refresh_token = token
    
    def clear_refresh_token(self):
        self.refresh_token = ''
    
    def set_active_user(self):
        self.set_active_user = True
        
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



