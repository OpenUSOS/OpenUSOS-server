import os


class Emails():

    def __init__(self, caller):
        self.caller = caller

    def send_email(self, Recepient, Subject, Content):
        try:
            Recepient_list = {Recepient}
            # We create the message:
            Message_id = self.caller.api.get('services/mailclient/create_message', subject=Subject, content=Content)
            # We update (create) recepient:
            self.caller.api.get('services/mailclient/update_recipients_group', message_id=Message_id["message_id"], emails=Recepient_list)

            # Then we refresh them:
            self.caller.api.get('services/mailclient/refresh_recipients', message_id=Message_id["message_id"] )
            # Finally, we send the message:
            test = {}
            # To make sure message was send (empty directory)
            test = self.caller.api.get('services/mailclient/send_message', message_id=Message_id["message_id"])
            if test:
                return 'N'
            return 'Y'
        except:
            return 'N'

    def get_emails(self):
        messages = []
        #We get all messages send by the user:
        messages = self.caller.api.get('services/mailclient/user', status='sent')
        #lista dokladnych informacji:
        lista = []
        for message in messages:
            element = {"id" : 1, "to" : 1, "subject": 1, "date": 1, "content":1}
            details = self.caller.api.get('services/mailclient/message', message_id= message["id"], fields = "id|subject|content|date")
            element["id"] = details["id"]
            element["subject"] = details["subject"]
            element["content"] = details["content"]
            element["date"] = details["date"]
            recepient_list = self.caller.api.get('services/mailclient/recipients', message_id= message["id"], fields = "email|user")
            element["to"] = recepient_list
            lista.append(element)
        return lista



