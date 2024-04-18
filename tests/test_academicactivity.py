import sys
from pathlib import Path
import unittest
import flet as ft
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.usosapi import USOSAPIConnection
from setup import App
from src.pages.academicactivity import AcademicActivity


class TestAcademicActivity(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls._app = None
        cls._page = None

    def test_display(self):
        activity = AcademicActivity(self._app, self._page)
        displayed = activity.display()
        self.assertIsInstance(displayed, ft.View)

    def test_get_data(self):
        with patch.object(USOSAPIConnection, 'get') as mock_get: # TODO needs changing
            to_return = [{'type': 'classgroup', 'start_time': '2024-04-19 10:30:00', 'end_time': '2024-04-19 12:45:00',
                          'name': {'en':'software engineering - laboratory', 'pl': 'inżynieria oprogramowania - laboratoria'}}]
            mock_get.return_value = to_return

            activity = AcademicActivity(self._app, self._page)
            value = activity.get_data()
            self.assertIsInstance(value,  list) # is value a dict
            self.assertListEqual(value, to_return) # is value the right list
            self.assertEqual(value, activity.data) # is value the same as grades.data (was data initialized properly)

    def test_display_buttons(self):
        activity = AcademicActivity(self._app, self._page)
        displayed = activity.display()
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
    TestAcademicActivity._app = app
    TestAcademicActivity._page = page
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAcademicActivity)
    unittest.TextTestRunner().run(suite)


def main(page: ft.Page):
    app = App(page)


ft.app(target=main)


