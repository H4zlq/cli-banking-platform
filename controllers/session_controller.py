import threading
from meta.singleton_meta import SingletonMeta
from services.session_service import SessionService


class SessionController(metaclass=SingletonMeta):
    session_service = SessionService(60)

    def __init__(self, authentication_view=None):
        self.authentication_view = authentication_view

    def get_session(self):
        return self.session_service.get_session()

    def start_session(self, data):
        self.session_service.set_session(data)

        if self.session_service.timer:
            self.session_service.timer.cancel()

        self.timer = threading.Timer(
            self.session_service.session_duration, self.end_session
        )

        self.timer.start()

    def end_session(self):
        self.session_service.end_session()

        if self.authentication_view:
            self.authentication_view.login()

        print("\nSession has ended due to timeout.")
