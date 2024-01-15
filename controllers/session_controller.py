import threading
from metas.session_meta import SessionMeta
from services.session_service import SessionService


class SessionController(metaclass=SessionMeta):
    session_service = SessionService(60)

    def __init__(self, authentication_view=None):
        self.authentication_view = authentication_view
        self.timer = None

    def get_session(self):
        return self.session_service.get_session()

    def start_session(self, data):
        self.session_service.set_session(data)
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(
            self.session_service.session_duration, self.end_session
        )
        self.timer.start()

    def end_session(self):
        self.session_service.end_session()

        if self.authentication_view:
            print("\nSession has ended due to timeout.")
            return self.authentication_view.login()

    def cancel_timer(self):
        self.session_service.cancel_timer()
