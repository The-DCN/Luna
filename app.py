import os
from flask import Flask, jsonify, request, escape
import werkzeug.exceptions as ex
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt
from authlib.jose.errors import ExpiredTokenError, DecodeError, BadSignatureError
from db import db
import functools
import utils
import datetime
import config
import sleep
from models import User

app = Flask(__name__)
app.config.from_object('config')

'''
    Things to be implemented here
    1. adding refresh token to http-only cookie
    2. need to add is_active and field to the user model
    3. add method that sets the refresh token to blank for a user if they log out 
    4. store ROLE field inside of jwt(done)
'''
    
'''
this decorator function checks if the jwt making the request hasn't been tampered with by malicious users or 
if the jwt making the request isn't expired.
'''
def login_required(method):
    @functools.wraps(method)
    def wrapper():            
        try: 
            
            token = request.headers.get('Authorization').split()[0]
            expired_token = db.collection(u'expired_tokens').document(token).get()
            
            if expired_token.exists:
                raise Exception
           
            else:
                #decode the token 
                encoded_token = bytes(token, 'utf-8')
                decoded = jwt.decode(encoded_token, app.config['KEY'])
                user = decoded['userid']
                user_doc = db.collection(u'users').document(user).get()
            
                if not user_doc.exists:
                    return utils.deactivate_token()
            
            return method(user_doc.to_dict())
        
        except Exception as e:
            print('used expired token')
            return jsonify({'message' : 'expired tokens cannot be used again'})     

        except DecodeError:
            print('decode error')
            return jsonify({'message':utils.deactivate_token(token)})
                # abort(400, message='Token is not valid please login again')
                
        except ExpiredTokenError:
            print('expired token error')
            return jsonify({'message' : utils.check_user_refresh_token(token)})
        
        except BadSignatureError:
            return jsonify({'message': 'Signature was bad.'})
            
        except ValueError:
            return jsonify({'message': 'You are required to be logged in to make this request'}) 
        
        except IndexError:
            return jsonify({'message': 'You are required to be logged in to make this request'})
  
    return wrapper

    

@app.route("/", methods=["GET"])
@login_required
def hello_world(user):
    sleep_record = db.collections(u'sleep').where('')
    return jsonify({"greeting": "hello world"})
 
                
@app.route("/api/login", methods=["POST"])
def user_login():
    
    try:
        valid_credentials = utils.validate_user_credentials(request.json['username'], request.json['password'])
        
        if not valid_credentials:
            return jsonify({'message': 'your credentials were invalid'})
        
        access_token = utils.create_access_token(request.json['username'], app.config['KEY'])
        refresh_token = utils.create_refresh_token(request.json['username'], app.config['KEY'])
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
    
    except Exception as e:
        return jsonify({'message': 'something went wrong while processing your request'})    
    


def invalid_credentials():
    return jsonify({'message': 'username or password is incorrect or does not exist'})

# Pending token authentication - WIP
@app.route("/sleep", methods=["GET"])
#@login_required
def getUserFeed(user):
    
    list = sleep.getLastSeven('jdoe123')
    
    #list = sleep.getLastSeven(user["username"])

    return jsonify({"message": list})


#when this is ran the access token is added to db of invalidated jwts 
@app.route("/logout", methods=["POST"])
def user_logout():
    try:
    # Bearer <token>
        token = request.headers['Authorization'].split(" ")[1]
        utils.deactivate_token(token)
        return jsonify({'message': ''})
    except:
        return  jsonify({'message': 'error occured'})

@app.route("/test", methods=["GET"])
def test_request():
    print(request.json['username'])
    return "Hello, world!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
