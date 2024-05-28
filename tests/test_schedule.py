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

    def test_get_schedule(self):
        self.caller.connector.resume(AT, ATS)
        with patch.object(USOSAPIConnection, 'get') as mock_get:
            testowa = [{"start_time" : '1987-01-01-21:37:00', "end_time" : "1987-01-01-22:37:00", "name" : "nie", "building_name" : "pieklo", "room_number" : "69"},
                        {"start_time" : '1984-01-01-21:37:00', "end_time" : "1984-01-01-22:37:00", "name" : "tak", "building_name" : "pieklo2", "room_number" : "420"}]
            mock_get.return_value = testowa
            data = self.caller.schedule.get_schedule("1987-01-01", 2)
            #print(data)
            lista = json.loads(data)
            self.assertIsInstance(lista, list)
            self.assertEqual(testowa, lista)
            


def run_tests(caller: Caller):
    TestUsersession.caller = caller
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUsersession)
    unittest.TextTestRunner().run(suite)

def main():
    caller = Caller(1, university_token["Uniwersytet Jagielloński"]["Consumer_key"], university_token["Uniwersytet Jagielloński"]["Consumer_secret"], university_token["Uniwersytet Jagielloński"]["url"])
    run_tests(caller)


main()