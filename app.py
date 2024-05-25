from flask import Flask, request
import uuid
import json
import asyncio

from tokeny.OpenUSOS_data import tokens

from src.usosapi import USOSAPIConnection
from src.usersession import Usersession
from src.pages.emails import Emails
from src.pages.grades import Grades
from src.pages.schedule import Schedule
from src.pages.surveys import Surveys
from src.pages.news import News


#One caller object is associated with one session, one user, and one id.
class Caller:

    def __init__(self, user_id, CK, CS, url):
        self.user_id = user_id  #Each caller is linked to one user.
        self.api = USOSAPIConnection(url, CK, CS)
        self.connector = Usersession(self) #Logging in/out
        self.email = Emails(self) #Email
        self.grades = Grades(self) #Grades
        self.schedule = Schedule(self)
        self.surveys = Surveys(self)
        self.news = News(self)
        

    
    def test(self):
        print("lalalalallalala")

caller_instances = {}

#One argument:
def handle_one_argument(arg1, used_caller):
    if arg1 == 'url':
        return used_caller.connector.url()
    elif arg1 == 'log_out':
        return used_caller.connector.log_out()
    elif arg1 == 'user_info':
        return used_caller.connector.user_info()
    elif arg1 == 'get_emails':
        return used_caller.email.get_emails()
    elif arg1 == 'get_grades':
        return used_caller.grades.get_grades()
    elif arg1 == 'get_tests':
        return used_caller.grades.get_tests()
    elif arg1 =='get_surveys':
        return used_caller.surveys.get_surveys()
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
    elif arg1 == 'get_schedule':
        return used_caller.schedule.get_schedule(arg2, arg3)
    elif arg1 =='answer_survey':
        return used_caller.surveys.answer_survey(arg2, arg3)
    elif arg1 == 'get_events':
        return used_caller.schedule.get_events(arg2, arg3)
    else:
        return 'Not a valid call, check the spelling or contact me.'
    
def handle_four_arguments(arg1, arg2, arg3, arg4, used_caller):
    if arg1 == 'send_email':
        return used_caller.email.send_email(arg2, arg3, arg4)
    elif arg1 == 'get_news':
        return used_caller.news.get_news(arg2, arg3, arg4)
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
3. id, query1 = resume, query2 [access token], query3 = [access token secret] ---- resumes the session.
returns 'Y' if was successful, and 'N' if not.
4. id, query1 = log_out, query2 empty ---- invalidates the access token.
---------
mail:
---------
5. id, query1 = send_email, query2 = [recepient], query3 = [subject], query4 = [content] ---- sends an email to
email adress given in [recepient], with subject given in [subject], and content given in [content].
returns 'Y' if message was send sucessfully, and 'N' if not.
6. id, query1 = get_emails ---- returns a list of mails send by user, where every element is a mail.
each element is a dict with: "id" : unique message id, "subject", "content", "date", 
and "to" - a list with two dicts:[ "email" - email of the recepient (or null), 
"user" - dict with information of the recepient: "first_name", "id", "last_name"]

example:
    {
        "content": "To jest test",
        "date": "2024-03-03 00:08:32",
        "id": "1780158",
        "subject": "Test",
        "to": [
            {
                "email": "oskar.kulinski@student.uj.edu.pl",
                "user": {
                    "first_name": "Oskar",
                    "id": "696969",
                    "last_name": "Kuliński"
                }
            }
        ]
    }
---------
grades:
---------
7. id, query1 = get_grades ---- returns a list, containing dicts with details of grades: "date", "author",
"value", "name" (the name of a course, like 'Metody numeryczne'), "term", "class_type" (WYK, LAB).
---------
schedule:
---------
8. id, query1 = get_schedule, query2 = [start_date], query3 = [num_of_days] ---- returns a list of dicts,
with activities starting from [start date] (%Y-%m-%d format), including num_of_days days.
each activity contains: {"start_time", "end_time", "name" : {"pl", "en"}, "building_name", "room_number"}
---------
info:
---------
9. id, query1 = user_info ---- returns a dict with user information {"first_name", "last_name", "photo_url" (200x200), "email"}
---------
tests:
---------
10. id, query1 = get_tests ---- returns a list of dictss, each one with: "term_id" (eg. 22/23Z) and "courses".
"courses" is a list of the courses that took place during the term. it contains "name" (eg. ASD, sieci) and "tests".
"tests" is a list of all tests within one course. it contains "name", "description", "points" (of user) "points_max", and "exercises".
"exercises is a list of all exercises within one test. it contains "name", "description", "points" (of user) and "points_max".
---------
surveys:
---------
11. id, query1 = get_surveys ----- returns a list of surveys. each one is a dict containing:
name, id, start_date, end_date, questions. each question is a dict with: id, number, display_text_html, allow_comment,
possible_answer. each possible anserw is a dict containing: id, display_text_html.

12. id, query1 = answer_survey, query2 = [id of a query you anserw], query3 = [anserw]. Anserws the specific survey. anserw should
be a JSON-formatted object, mapping question IDs to their answers, {"question1_id": {"answers": ["possible_answer1_id",
"possible_answer2_id", ...], "comment": "comment or null"}, "question2_id": ...}
Note, that all values of this objects are strings (because the IDs of possible answers are strings).
If comment should be left empty or the question does not allow comments, null has be passed in comment field.
----------
events:
----------
13. id, query1 = get_events, query2 = [from_date], query3 = [to_date], gets list of events begining from and ending at.
each object in a list is a dict with "name" that has the name of a programme from which the event is, and "list"
with the list of the events. each event has a name, start_date, end_date, type, is_day_off (telling if it's a day of).
----------
news:
----------
14. id, query1 = get_news, query2 = [from_date], query3 = [start], query4 = [num] (100 <)
returns a dict with: 
"next_page" - true if there are more items. 
"total" - int showing how many items were matched
"items" a list of items. each item has just one field, "article" 
(kinda usless, but supposedly they can add more types of items in the future).
each article contains: name, author, publication_date, title, headline_html, content_html.

"""



#It has to be in one function, since it gets called everytime GET is made:
@app.route('/api', methods = ['GET'])
async def call():
    #These can be empty:
    id = request.args.get('id')
    query1 = request.args.get('query1', None)
    query2 = request.args.get('query2', None)
    query3 = request.args.get('query3', None)
    query4 = request.args.get('query4', None)

    if id not in caller_instances:
        return 'User not authenticated'
    used_caller = caller_instances[id]
    #If three arguments given
    if(query1 and query2 and query3 and query4):
        query1 = str(query1)
        query2 = str(query2)
        query3 = str(query3)
        query4 = str(query4)
        return handle_four_arguments(query1,query2, query3, query4, used_caller)
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
async def login():
    #We take the target url:
    query1 = request.args.get('query1', None)
    if(query1 is None):
        return "University required"
    if query1 not in tokens.university_token:
        return "Not a valid uniersity, check the spelling or contact me"
    
    # We create a unique id that the user will use:
    user_id = generate_unique_id()
    caller_instances[user_id] = Caller(user_id, tokens.university_token[query1]["Consumer_key"], 
                                       tokens.university_token[query1]["Consumer_secret"], tokens.university_token[query1]["url"])
    
    return user_id

if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=5000)
    #app.run(host='0.0.0.0' , port=20117)

#{"AT": "2yDqSfspnT3jtauhCtjH", "ATS": "7ZHE23cNvWtwRxFfctS5BQw5HC8tNru2DDKrfkaQ"}