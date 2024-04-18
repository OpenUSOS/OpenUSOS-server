import sys
from pathlib import Path
import unittest
import flet as ft
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.usosapi import USOSAPIConnection
from setup import App
from src.pages.user import User


class TestUser(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls._app = None
        cls._page = None

    def test_display(self):
        user = User(self._app, self._page)
        displayed = user.display()
        self.assertIsInstance(displayed, ft.View)

    def test_get_data(self):
        with patch.object(USOSAPIConnection, 'get') as mock_get: # TODO needs changing

            mock_get.return_value = {'id': '123456', 'first_name': 'aaa', 'last_name' : 'bbb'}

            user = User(self._app, self._page)
            value = user.get_data()
            self.assertIsInstance(value,  dict) # is value a dict
            self.assertDictEqual(value, {'id': '123456', 'first_name': 'aaa', 'last_name' : 'bbb'})
            #  is value the right dict
            self.assertEqual(value, user.data) # is value the same as grades.data (was data initialized properly)

    def test_display_buttons(self):
        user = User(self._app, self._page)
        displayed = user.display()
        control_list = [displayed.controls]
        while len(control_list) > 0:
            current_control = control_list.pop()
            control_list.extend(current_control.controls)
            if (isinstance(current_control, ft.ElevatedButton) or isinstance(current_control, ft.FloatingActionButton)
                    or isinstance(current_control, ft.TextButton) or isinstance(current_control, ft.IconButton)
                    or isinstance(current_control, ft.PopupMenuButton) or isinstance(current_control, ft.OutlinedButton)
                    or isinstance(current_control, ft.CupertinoButton)):
                self.assertFalse(current_control.on_click is None)
                self.assertTrue(callable(current_control.on_click))


def run_tests(app: App, page: ft.Page):
    TestUser._app = app
    TestUser._page = page
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
    unittest.TextTestRunner().run(suite)


def main(page: ft.Page):
    app = App(page)


if __name__ == "__main__":
    ft.app(target=main)


