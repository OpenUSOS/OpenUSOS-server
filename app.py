from flask import Flask, request
import uuid

from src.usosapi import USOSAPIConnection
from src.usersession import Usersession

Usosapi_base_url = 'https://apps.usos.uj.edu.pl/'

# Consumer Key to use.
Consumer_key = '748apdbMm3Ggh6KGXMyp'
Consumer_secret = 'Y33JYY3vgjNym6aFP5qnxcMtE7WrejLt8VDjWS87'


class Caller:

    def __init__(self, user_id):
        self.user_id = user_id  #Each caller is linked to one user.
        self.api = USOSAPIConnection(Usosapi_base_url, Consumer_key, Consumer_secret)
        self.connector = Usersession(self)
    
    def test(self):
        print("lalalalallalala")
caller_instances = {}

def handle_one_argument(arg1, used_caller):
    #Funkcje caller:
    if arg1 == 'try_logging_in':
        return used_caller.connector.try_logging_in()
    elif arg1 == 'remember_me':
        return used_caller.connector.remember_me()
    elif arg1 == 'log_out':
        return used_caller.connector.logout()
    else:
        return 'Not a valid call, check the spelling or contact me.'



def handle_two_arguments(arg1, arg2, used_caller):
    if arg1 == 'log_in':
        arg2 = int(arg2)
        return used_caller.connector.login(arg2)
    else:
        return 'Not a valid call, check the spelling or contact me.'




#I am writing all api calls here:
#calls should look like http://127.0.0.1:5000/api?id=12456772&query1=a&query2=bar or http://127.0.0.1:5000/api?id=12456772&query1=223456

#IMPORTANT! First, you need to create a session using http://127.0.0.1:5000/login. It will return your id, that
#Should be kept secret. Then, when using other methods use this id.

"""
1. id, query1 = try_logging_in, query2 empty ---- returns a string, url which has to be used to log in.
WARNING! If option remember me was used, it just refreshes the session.

2. id, query1 = log_in, query2 = PIN (The value)  ---- logging the user in
3. id, query1 = remember_me, query2 empty ---- keeps the user logged in
4. id, query1 = log_out, query2 empty ---- logging user out


"""
app = Flask(__name__)


#It has to be in one function, since it gets called everytime GET is made:
@app.route('/api', methods = ['GET'])
def call():
    #These can be empty:
    id = request.args.get('id')
    query1 = request.args.get('query1', None)
    query2 = request.args.get('query2', None)

    if id not in caller_instances:
        return 'User not authenticated'
    used_caller = caller_instances[id]
    #If two arguments given
    if(query1 and query2):
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