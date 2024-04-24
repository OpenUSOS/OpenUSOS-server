import flet as ft
from .interface import ViewInterface
import os

class Usersession(ViewInterface):

    def __init__(self, app, page: ft.Page):
        pass
    
    #Trying to log in without token:
    def no_url(self) -> bool:
        if os.path.exists("token.txt"): #If token exists:
            with open("token.txt", "r") as file:
                line1 = file.readline()
                AT = str(line1.strip())
                line2 = file.readline()
                ATS = str(line2.strip())
        else: 
            return False
        
        if(self.app.api.set_access_data(AT, ATS)):
            return True
        else:
            return False

    def login(self):
        #We try to login without url
        if(self.no_url() == False):
            #If we can't
            AuthURL = self.app.api.get_authorization_url()
            print(AuthURL) # Pass it to user somehow
            PIN = input('What is the PIN code? ')
            PIN.replace(" ", "")
            # Authorization:
            self.app.api.authorize_with_pin(PIN)
            while (self.app.api.is_authorized() == False):
                PIN = input('Wrong PIN. Try again. ')
                PIN.replace(" ", "")
                # Authorization:
                self.app.api.authorize_with_pin(PIN)
            

    def logout(self):
        self.app.api.logout()
    
    def display(self):
        return super().display()
    
    def get_data(self) -> dict:
        return super().get_data()


