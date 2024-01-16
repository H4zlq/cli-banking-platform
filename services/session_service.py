from meta.singleton_meta import SingletonMeta


class SessionService(metaclass=SingletonMeta):
    def __init__(self, session_duration):
        self.data = None
        self.session_duration = session_duration
        self.timer = None

    def get_session(self):
        return self.data

    def set_session(self, data):
        self.data = data

    def end_session(self):
        self.data = None
        self.timer = None

    def cancel_timer(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
