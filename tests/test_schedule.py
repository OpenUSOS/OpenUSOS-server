import sys
from pathlib import Path
import unittest
import flet as ft
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.usosapi import USOSAPIConnection
from setup import App
from src.pages.schedule import Schedule


class TestSchedule(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls._app = None
        cls._page = None

    def test_display(self):
        schedule = Schedule(self._app, self._page)
        displayed = schedule.display()
        self.assertIsInstance(displayed, ft.View)

    def test_get_data(self):
        with patch.object(USOSAPIConnection, 'get') as mock_get:  # TODO needs changing
            to_return = [{
                "start_time": "2024-04-25 10:15:00",
                "end_time": "2024-04-25 11:45:00",
                "name": {
                    "pl": "Rachunek prawdopodobieństwa i statystyka - Wykład",
                    "en": "Probability and Statistics - Lecture"
                }
            },
                {
                    "start_time": "2024-04-25 11:30:00",
                    "end_time": "2024-04-25 13:00:00",
                    "name": {
                        "pl": "Język hiszpański - B1 - 30 godzin/2 semestr - Lektorat",
                        "en": "Spanish Interfaculty Group - Foreign language class"
                    }
                }]
            mock_get.return_value = to_return

            schedule = Schedule(self._app, self._page)
            value = schedule.get_data()
            self.assertIsInstance(value, list)  # is value a dict
            self.assertListEqual(value, to_return)  # is value the right dict
            self.assertEqual(value, schedule.data)  # is value the same as grades.data (was data initialized properly)

    def test_display_buttons(self):
        schedule = Schedule(self._app, self._page)
        displayed = schedule.display()
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
    TestSchedule._app = app
    TestSchedule._page = page
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSchedule)
    unittest.TextTestRunner().run(suite)


def main(page: ft.Page):
    app = App(page)


if __name__ == "__main__":
    ft.app(target=main)
