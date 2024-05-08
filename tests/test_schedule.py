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

    def test_get_schedule(self):
        self.caller.connector.resume(AT, ATS)
        with patch.object(USOSAPIConnection, 'get') as mock_get:
            mock_get.return_value = {[{"start_time" : '1987-01-01-21:37:00', "end_time" : "1987-01-01-22:37:00", "name" : "nie"}]}
            data = self.caller.schedule.get_schedule("1987-01-01", 2)
            print(data)
            list = json.loads(data)


def run_tests(caller: Caller):
    TestUsersession.caller = caller
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUsersession)
    unittest.TextTestRunner().run(suite)

def main():
    caller = Caller(1)
    run_tests(caller)


main()