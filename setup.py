import flet as ft
from src.usosapi import USOSAPIConnection
from src.usersession import Usersession
from src.pages.grades import Grades

Usosapi_base_url = 'https://apps.usos.uj.edu.pl/'

# Consumer Key to use.
Consumer_key = '748apdbMm3Ggh6KGXMyp'
Consumer_secret = 'Y33JYY3vgjNym6aFP5qnxcMtE7WrejLt8VDjWS87'

def main(page: ft.Page):
    App(page)

class App:

    def __init__(self, page: ft.Page):
        self.api = USOSAPIConnection(Usosapi_base_url, Consumer_key, Consumer_secret)
        #self.page = page
        self.connector = Usersession(self, page)
    
    def test(self):
        print("lalalalallalala")


ft.app(target=main)