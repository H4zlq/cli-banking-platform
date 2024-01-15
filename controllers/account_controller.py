from services.account_service import AccountService


class AccountController:
    account_service = AccountService()

    def update_password(self, username, password):
        self.account_service.update_password(username, password)
