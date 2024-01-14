import time


class TimeUtil:
    @staticmethod
    def get_timestamp():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
