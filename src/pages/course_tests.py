import flet as ft
from ..interface import ViewInterface


class Tests(ViewInterface):

    def __init__(self, app, page: ft.Page):
        self.data = self.get_data()
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def display(self):
        raise NotImplementedError



