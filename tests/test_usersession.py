import sys
from pathlib import Path
import unittest
import flet as ft
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.usosapi import USOSAPIConnection
from setup import App
from src.usersession import Usersession

class TestUsersession(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls._app = None
        cls._page = None

    def test_login(self):
        connector = Usersession(self._app, self._page)
        connector.login()
        self.assertTrue(connector.app.api.test_connection())

    def test_login(self):
        connector = Usersession(self._app, self._page)
        connector.login()
        connector.logout()
        self.assertFalse(connector.app.api.test_connection())


def run_tests(app: App, page: ft.Page):
    TestUsersession._app = app
    TestUsersession._page = page
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUsersession)
    unittest.TextTestRunner().run(suite)

def main(page: ft.Page):
    app = App(page)


if __name__ == "__main__":
    ft.app(target=main)