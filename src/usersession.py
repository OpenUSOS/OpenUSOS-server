import os

class Usersession():

    def __init__(self, caller):
        self.caller = caller
    
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
        
        if(self.caller.api.set_access_data(AT, ATS)):
            return True
        else:
            return False
        
    # Function that will save Access token of user, allowing us to log in without authorization:
    def remember_me(self):
        if os.path.exists("usos_token.txt"):
            # First we delete this file if it exists:
            os.remove("usos_token.txt")
        AT, ATS = self.caller.api.get_access_data()
        with open("token.txt", "w") as file:
            file.write(AT)
            file.write("\n")
            file.write(ATS)
        return 'You will be kept logged in!'

    def login(self, PIN):
        # Authorization:
        self.caller.api.authorize_with_pin(PIN)
        if(self.caller.api.is_authorized() == False):
            return 'Wrong PIN, try again'
        else:
            return 'You are now logged in'

    def try_logging_in(self):
        if(self.no_url() == False):
            AuthURL = self.caller.api.get_authorization_url()
            return AuthURL # Pass it to user somehow
        else:
            return 'You are already logged in!'
            

    def logout(self):
        self.caller.api.logout()
        return 'You are now logged out!'