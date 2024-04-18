import sys
from pathlib import Path
import unittest
import flet as ft
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.usosapi import USOSAPIConnection
from setup import App
from src.pages.home import Home


class TestHome(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(cls):
        cls._app = None
        cls._page = None

    def test_display(self):
        home = Home(self._app, self._page)
        displayed = home.display()
        self.assertIsInstance(displayed, ft.View)

    def test_display_buttons(self):
        home = Home(self._app, self._page)
        displayed = home.display()
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
    TestHome._app = app
    TestHome._page = page
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHome)
    unittest.TextTestRunner().run(suite)


def main(page: ft.Page):
    app = App(page)
    run_tests(app, app.page)


ft.app(target=main)

