import flet as ft
from src.usosapi import USOSAPIConnection
from src.pages.grades import Grades


def main(page: ft.Page):
    App(page)


class App:

    def __init__(self, page: ft.Page):
        self.api = USOSAPIConnection()
        self.page = page
        raise NotImplementedError


ft.app(target=main)