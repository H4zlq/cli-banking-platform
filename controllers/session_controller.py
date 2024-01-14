from models.session_model import Session


class SessionController(Session):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SessionController, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.user = None

    def get_session(self):
        return self.user

    def set_session(self, user):
        self.user = user
