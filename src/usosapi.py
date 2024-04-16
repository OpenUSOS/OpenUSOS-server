class USOSAPIConnection():
    pass
    def __init__(self):
        pass
    #-----------------------------------------------------------------------------------
    def _generate_request_token(self):
        pass

    def is_anonymous(self) -> bool:
        pass

    def is_authorized(self) -> bool:
        pass

    def test_connection(self) -> bool:
        pass

    def get_authorization_url(self) -> str:
        pass

    def authorize_with_pin(self, pin: str):
       pass

    def get_access_data(self) -> tuple:
        pass

    def set_access_data(self) -> bool:
       pass

    def get(self):
        pass

    def logout(self):
        pass

    def current_identity(self):
        pass