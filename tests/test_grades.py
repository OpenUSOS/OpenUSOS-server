import sys
from pathlib import Path
import unittest
from unittest.mock import patch
import json

sys.path.append(str(Path(__file__).resolve().parents[1]))
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

    def test_get_grades(self):
        self.caller.connector.resume(AT, ATS)
        data = self.caller.grades.get_grades()
        #print(data)
        lista = json.loads(data)
        if {'term': '23/24Z', 'name': 'Analiza matematyczna 2', 'author': {'id': '54', 'first_name': 'Anna', 'last_name': 'Ochal'},
             'value': '4,5', 'date': '2024-02-01 22:22:23', 'class_type': 'WYK'} in lista:
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
