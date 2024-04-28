from flask import Flask, request
import uuid
import json

from src.usosapi import USOSAPIConnection
from src.usersession import Usersession

Usosapi_base_url = 'https://apps.usos.uj.edu.pl/'

# Consumer Key to use.
Consumer_key = '748apdbMm3Ggh6KGXMyp'
Consumer_secret = 'Y33JYY3vgjNym6aFP5qnxcMtE7WrejLt8VDjWS87'

#One caller object is associated with one session, one user, and one id.
class Caller:

    def __init__(self, user_id):
        self.user_id = user_id  #Each caller is linked to one user.
        self.api = USOSAPIConnection(Usosapi_base_url, Consumer_key, Consumer_secret)
        self.connector = Usersession(self)
    
    def test(self):
        print("lalalalallalala")

caller_instances = {}

#One argument:
def handle_one_argument(arg1, used_caller):
    if arg1 == 'url':
        return used_caller.connector.url()
    elif arg1 == 'log_out':
        return used_caller.connector.log_out()
    else:
        return 'Not a valid call, check the spelling or contact me.'


#Two arguments:
def handle_two_arguments(arg1, arg2, used_caller):
    if arg1 == 'log_in':
        arg2 = int(arg2)
        return used_caller.connector.log_in(arg2)
    else: 
        return 'Not a valid call, check the spelling or contact me.'
    
def handle_three_arguments(arg1, arg2, arg3, used_caller):
    if arg1 == 'resume':
        return used_caller.connector.resume(arg2, arg3)
    else:
        return 'Not a valid call, check the spelling or contact me.'

app = Flask(__name__)

#I am writing all api calls here:
#calls should look like http://127.0.0.1:5000/api?id=12456772&query1=a&query2=bar or http://127.0.0.1:5000/api?id=12456772&query1=223456
#They can have up to 4 arguments. first is always id, then query(nr of query)
#IMPORTANT! First, you need to create a session using http://127.0.0.1:5000/login. It will return your id, that
#Should be kept secret. Then, when using other methods use this id.

"""
logging in/out:
---------
1. id, query1 = url, query2 empty ---- returns a string, url which has to be used to log in.
2. id, query1 = log_in, query2 = PIN (The value)  ---- logging the user in. 
returns dict {'AT', ATS'} with [access token] and [access token secret] used to resume the session, or 'N' if not succesful
3. id, query1 = resume, query2 [access token], query3 = [access token secret] ---- keeps the 
user logged in. returns 'Y' if was successful, and 'N' if not.
4. id, query1 = log_out, query2 empty ---- invalidates the access token.
---------



"""


#It has to be in one function, since it gets called everytime GET is made:
@app.route('/api', methods = ['GET'])
def call():
    #These can be empty:
    id = request.args.get('id')
    query1 = request.args.get('query1', None)
    query2 = request.args.get('query2', None)
    query3 = request.args.get('query3', None)

    if id not in caller_instances:
        return 'User not authenticated'
    used_caller = caller_instances[id]
    #If three arguments given
    if(query1 and query2 and query3):
        query1 = str(query1)
        query2 = str(query2)
        query3 = str(query3)
        return handle_three_arguments(query1,query2, query3, used_caller)
    #If two arguments given
    elif(query1 and query2):
        query1 = str(query1)
        query2 = str(query2)
        return handle_two_arguments(query1,query2, used_caller)
    #If one argument given
    elif (query1):
        query1 = str(query1)
        return handle_one_argument(query1, used_caller)

def generate_unique_id():
    while True:
        unique_id = str(uuid.uuid4())
        if unique_id not in caller_instances:
            return unique_id


@app.route('/login', methods=['GET'])
def login():
    # We create a unique id that the user will use:
    user_id = generate_unique_id()
    caller_instances[user_id] = Caller(user_id)  # Initialize Caller instance with user_id
    return user_id

if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=5000)