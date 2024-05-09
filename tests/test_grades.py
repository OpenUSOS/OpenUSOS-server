import sys
from pathlib import Path
import unittest
from unittest.mock import patch
import json

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.usosapi import USOSAPIConnection


from app import Caller

AT = 'YVy5wT7gXJJrTs3QMq25'
ATS = 'uvBDbNCQzbEAyVFj6emnKvSTGSxKnVqxgYRMn2Ba'

class TestUsersession(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls.caller = Caller(123)

    def test_get_grades(self):
        self.caller.connector.resume(AT, ATS)
        data = self.caller.grades.get_grades()
        #print(data)
        lista = json.loads(data)
        if {"date": "2024-02-01-22:22", "author": {"id": "54", "first_name" : "Anna", "last_name": "Ochal"}, "value" : "4.5",
            "name": "Analiza matematyczna 2", "type": "WYK"} in lista:
            pass
        else:
            self.assertTrue(1 == 2)
            


def run_tests(caller: Caller):
    TestUsersession.caller = caller
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUsersession)
    unittest.TextTestRunner().run(suite)

def main():
    caller = Caller(1)
    run_tests(caller)


main()
