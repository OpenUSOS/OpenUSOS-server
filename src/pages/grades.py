import flet as ft
from ..interface import ViewInterface


class Grades(ViewInterface):

    def __init__(self, app, page: ft.Page):
        self.data = dict
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def display(self) -> ft.View:
        raise NotImplementedError



