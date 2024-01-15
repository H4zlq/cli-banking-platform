from services.log_service import LogService


class LogController:
    log_service = LogService()

    def get_logs(self):
        return self.log_service.get_logs()

    def insert_logs(self, id, action, date):
        return self.log_service.insert_logs(id, action, date)
