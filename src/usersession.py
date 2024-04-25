import flet as ft
from .interface import ViewInterface
import os

class Usersession(ViewInterface):

    def __init__(self, app, page: ft.Page):
        self.app = app
        self.page = page
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
        
    # Function that will save Access token of user, allowing us to log in without authorization:
    def Remember_me(self):
        if os.path.exists("usos_token.txt"):
            # First we delete this file if it exists:
            os.remove("usos_token.txt")
        AT, ATS = self.app.api.get_access_data()
        with open("token.txt", "w") as file:
            file.write(AT)
            file.write("\n")
            file.write(ATS)

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
            anserw = input('Do you want not to be logged out? (Y/N).' )
            while (anserw != 'Y' and anserw != 'N'):
                anserw = input('Not a Y or N. Try again')
            if (anserw == 'Y'):
                self.Remember_me()
            

    def logout(self):
        self.app.api.logout()
    
    def display(self):
        return super().display()
    
    def get_data(self) -> dict:
        return super().get_data()


