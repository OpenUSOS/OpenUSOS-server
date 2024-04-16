import unittest

from src.pages.grades import Grades
class TestGrades(unittest.TestCase):

    def test_display(self):
        grades = Grades()
        displayed = grades.display()
        self.assertIsInstance()