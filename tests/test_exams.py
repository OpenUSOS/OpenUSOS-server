import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest
import flet as ft
from src.usosapi import USOSAPIConnection
from setup import App
from src.pages.grades import Grades



class TestGrades(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(self):
        self._app = None
        self._page = None

    def test_display(self):
        grades = Grades(self._app, self._page)
        displayed = grades.display()
        self.assertIsInstance(displayed, ft.View)

def run_tests(app: App, page: ft.Page):
    TestGrades._app = app
    TestGrades._page = page
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGrades)
    unittest.TextTestRunner().run(suite)


def main(page: ft.Page):
    app = App(page)


if __name__ == "__main__":
    ft.app(target=main)