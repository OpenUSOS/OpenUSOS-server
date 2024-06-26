import os
import json

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
        try: 
            self.caller.api.authorize_with_pin(PIN)
            # We check if session is now authorized:
            if(self.caller.api.is_authorized() == False):
                return 'N'
            else:
                AT, ATS = self.caller.api.get_access_data()
                mydict = {'AT': AT, "ATS": ATS}
                json_string = json.dumps(mydict)
                return json_string
        except:
            return 'N'

    def url(self):
        AuthURL = self.caller.api.get_authorization_url()
        return AuthURL # Pass it to user somehow
            
    def log_out(self):
        self.caller.api.logout() #invalidate the token.
        return 'Access tokens invalidated!'
    
    def user_info(self):
        data = self.caller.api.get('services/users/user', fields='first_name|last_name|email|photo_urls[200x200]')
        info = {}
        info["first_name"] = data["first_name"]
        info["last_name"] = data["last_name"]
        info["photo_url"] = data["photo_urls"]
        info["email"] = data["email"]
        json_string = json.dumps(info)
        return json_string
