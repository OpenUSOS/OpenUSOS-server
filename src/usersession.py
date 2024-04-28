import os

class Usersession():

    def __init__(self, caller):
        self.caller = caller
    
    #Trying to log in without token:
    def resume(self, AT, ATS) -> bool:
        if(self.caller.api.set_access_data(AT, ATS)):
            return 'Y'
        else:
            return 'N'

    def log_in(self, PIN):
        # Authorization:
        self.caller.api.authorize_with_pin(PIN)
        if(self.caller.api.is_authorized() == False):
            return 'N'
        else:
            AT, ATS = self.caller.api.get_access_data()
            return AT, ATS

    def url(self):
        AuthURL = self.caller.api.get_authorization_url()
        return AuthURL # Pass it to user somehow
            
    def log_out(self):
        self.caller.api.logout() #invalidate the token.
        return 'Access tokens invalidated!'