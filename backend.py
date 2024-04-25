from flask import Flask, request

from src.usosapi import USOSAPIConnection
from src.usersession import Usersession
from src.pages.grades import Grades

Usosapi_base_url = 'https://apps.usos.uj.edu.pl/'

# Consumer Key to use.
Consumer_key = '748apdbMm3Ggh6KGXMyp'
Consumer_secret = 'Y33JYY3vgjNym6aFP5qnxcMtE7WrejLt8VDjWS87'



class Caller:

    def __init__(self):
        self.api = USOSAPIConnection(Usosapi_base_url, Consumer_key, Consumer_secret)
        self.connector = Usersession(self)
    
    def test(self):
        print("lalalalallalala")


caller = Caller()

def handle_one_argument(arg1):
    #Funkcje caller:
    if arg1 == 'try_logging_in':
        return caller.connector.try_logging_in()
    elif arg1 == 'remember_me':
        return caller.connector.remember_me()
    elif arg1 == 'log_out':
        return caller.connector.logout()
    else:
        return 'Not a valid call, check the spelling or contact me.'



def handle_two_arguments(arg1, arg2):
    if arg1 == 'log_in':
        arg2 = int(arg2)
        return caller.connector.login(arg2)
    else:
        return 'Not a valid call, check the spelling or contact me.'




#I am writing all api calls here:
#calls should look like http://127.0.0.1:5000/api?query1=a&query2=bar or http://127.0.0.1:5000/api?query1=223456
"""
1. query1 = try_logging_in, query2 empty ---- returns a string, url which has to be used to log in.
WARNING! If option remember me was used, it just refreshes the session.

2. query1 = log_in, query2 = PIN (The value)  ---- logging the user in
3. query1 = remember_me, query2 empty ---- keeps the user logged in
4. query1 = log_out, query2 empty ---- logging user out


"""
app = Flask(__name__)

#It has to be in one function, since it gets called everytime GET is made:
@app.route('/api', methods = ['GET'])
def call():
    #These can be empty:
    query1 = request.args.get('query1', None)
    query2 = request.args.get('query2', None)
    #If two arguments given
    if(query1 and query2):
        query1 = str(query1)
        query2 = str(query2)
        return handle_two_arguments(query1,query2)
    #If one argument given
    elif (query1):
        query1 = str(query1)
        return handle_one_argument(query1)

if __name__ == "__main__":
    app.run()