import sys
from pathlib import Path
import unittest
import flet as ft
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))


from setup import App

class TestUsersession(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls._page = ft.Page
        cls._app = App(cls._page)

    def test_login(self):
        self._app.connector.login()
        self.assertTrue(self._app.api.is_authorized())

    def test_logout(self):
        self._app.connector.login()
        self._app.connector.logout()
        self.assertFalse(self._app.api.is_authorized())


def run_tests(app: App, page: ft.Page):
    TestUsersession._app = app
    TestUsersession._page = page
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUsersession)
    unittest.TextTestRunner().run(suite)

def main(page: ft.Page):
    app = App(page)
    run_tests(app, page)


if __name__ == "__main__":
    ft.app(target=main)