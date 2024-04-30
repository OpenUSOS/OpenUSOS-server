import os


class Emails():

    def __init__(self, caller):
        self.caller = caller

    def send_email(self, Recepient, Subject, Content):
        Recepient_list = {Recepient}
        # We create the message:
        Message_id = self.caller.api.get('services/mailclient/create_message', subject=Subject, content=Content)
        # We update (create) recepient:
        self.caller.api.get('services/mailclient/update_recipients_group', message_id=Message_id["message_id"], emails=Recepient_list)
        # Then we refresh them:
        self.caller.api.get('services/mailclient/refresh_recipients', message_id=Message_id["message_id"] )

        # Finally, we send the message:
        self.caller.api.get('services/mailclient/send_message', message_id=Message_id["message_id"])
        return 'wyslano'

    def display(self):
        raise NotImplementedError



