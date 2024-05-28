import sys
from pathlib import Path
import unittest
from unittest.mock import patch
import json

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.usosapi import USOSAPIConnection
from tokeny.OpenUSOS_data.tokens import university_token


from app import Caller

AT = '2yDqSfspnT3jtauhCtjH'
ATS = '7ZHE23cNvWtwRxFfctS5BQw5HC8tNru2DDKrfkaQ'

class TestUsersession(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls.caller = Caller(123, university_token["Uniwersytet Jagielloński"]["Consumer_key"], university_token["Uniwersytet Jagielloński"]["Consumer_secret"], university_token["Uniwersytet Jagielloński"]["url"])


    def test_get_email(self):
        self.caller.connector.resume(AT, ATS)
        data = self.caller.email.get_emails()
        #print(data)
        lista = json.loads(data)
        if {"id": "1780158", "to": [{"email": "oskar.kulinski@student.uj.edu.pl", "user": None}],
             "subject": "Test", "date": "2024-03-03 00:08:32", "content": "To jest test"} in lista:
            pass
        else:
            self.assertTrue(1 == 2)
        
            


def run_tests(caller: Caller):
    TestUsersession.caller = caller
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUsersession)
    unittest.TextTestRunner().run(suite)

def main():
    caller = Caller(1, university_token["Uniwersytet Jagielloński"]["Consumer_key"], university_token["Uniwersytet Jagielloński"]["Consumer_secret"], university_token["Uniwersytet Jagielloński"]["url"])
    run_tests(caller)


main()