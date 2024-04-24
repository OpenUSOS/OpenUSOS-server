import flet as ft
from .interface import ViewInterface
from ..setup import App

class Usersession(ViewInterface):

    def __init__(self, app, page: ft.Page):
        raise NotImplementedError
    
    def login(self):
        raise NotImplementedError
    
    def logout(self):
        raise NotImplementedError
    


