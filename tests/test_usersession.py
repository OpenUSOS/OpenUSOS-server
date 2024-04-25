import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))


from backend import Caller

class TestUsersession(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls.caller = Caller()

    def test_login(self):
        url = self.caller.connector.try_logging_in()
        print(url)
        PIN = input("What is the PIN?")
        self.caller.connector.login(PIN)
        self.caller.connector.remember_me()
        self.assertTrue(self.caller.api.is_authorized())

    def test_logout(self):
        url = self.caller.connector.try_logging_in()
        print(url)
        self.caller.connector.logout()
        self.assertFalse(self.caller.api.is_authorized())


def run_tests(caller: Caller):
    TestUsersession.caller = caller
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUsersession)
    unittest.TextTestRunner().run(suite)

def main():
    caller = Caller()
    run_tests(caller)


main()