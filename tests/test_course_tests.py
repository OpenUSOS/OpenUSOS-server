import sys
from pathlib import Path
import unittest
import flet as ft
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.usosapi import USOSAPIConnection
from setup import App
from src.pages.course_tests import Tests


class TestTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls._app = None
        cls._page = None

    def test_display(self):
        tests = Tests(self._app, self._page)
        displayed = tests.display()
        self.assertIsInstance(displayed, ft.View)

    def test_get_data(self):
        with patch.object(USOSAPIConnection, 'get') as mock_get:
            mock_get.return_value = {'22/23': {}, '23/24': {}}

            tests = Tests(self._app, self._page)
            value = tests.get_data()
            self.assertIsInstance(value,  dict) # is value a dict
            self.assertDictEqual(value, {'22/23': {}, '23/24': {}}) # is value the right dict
            self.assertEqual(value, tests.data) # is value the same as data (was data initialized properly)

    def test_display_buttons(self):
        tests = Tests(self._app, self._page)
        displayed = tests.display()
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
    TestTests._app = app
    TestTests._page = page
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTests)
    unittest.TextTestRunner().run(suite)


def main(page: ft.Page):
    app = App(page)


if __name__ == "__main__":
    ft.app(target=main)


