import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))


from app import Caller

AT = '1'
ATS = '2'

class TestUsersession(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls.caller = Caller(123)

    def test_login(self):
        url = self.caller.connector.url()
        print(url)
        PIN = input("What is the PIN?")
        dict = self.caller.connector.log_in(PIN)
        AT = dict['AT']
        ATS = dict['ATS']
        self.assertTrue(self.caller.api.is_authorized())

    def test_logout(self):
        self.caller.connector.resume(AT, ATS)
        self.caller.connector.log_out()
        self.assertFalse(self.caller.api.is_authorized())


def run_tests(caller: Caller):
    TestUsersession.caller = caller
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUsersession)
    unittest.TextTestRunner().run(suite)

def main():
    caller = Caller(1)
    run_tests(caller)


main()