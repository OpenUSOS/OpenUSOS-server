import sys
from pathlib import Path
import unittest
import flet as ft
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.usosapi import USOSAPIConnection
from setup import App
from src.pages.exams import Exams



class TestExams(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect_app()

    @classmethod
    def connect_app(self):
        self._app = None
        self._page = None

    def test_display(self):
        exams = Exams(self._app, self._page)
        displayed = exams.display()
        self.assertIsInstance(displayed, ft.View)

    def test_get_data(self):
        with patch.object(USOSAPIConnection, 'get') as mock_get:
            mock_get.return_value = {'22/23': {}, '23/24': {}}

            exams = Exams(self._app, self._page)
            self.assertIsInstance(exams.data,  dict)
            self.assertDictEqual(exams.data, {'22/23': {}, '23/24': {}})



def run_tests(app: App, page: ft.Page):
    TestGrades._app = app
    TestGrades._page = page
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGrades)
    unittest.TextTestRunner().run(suite)


def main(page: ft.Page):
    app = App(page)


if __name__ == "__main__":
    ft.app(target=main)


