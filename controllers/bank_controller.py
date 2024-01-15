from services.bank_service import BankService
from services.log_service import LogService
from services.transaction_service import TransactionService


class BankController:
    bank_service = BankService()
    log_service = LogService()
    transaction_service = TransactionService()

    def get_balance(self, username):
        return self.bank_service.get_balance(username)

    def deposit(self, username, amount):
        return self.bank_service.deposit(username, amount)

    def withdraw(self, username, amount):
        return self.bank_service.withdraw(username, amount)

    def transfer(self, username, amount, recipient):
        return self.bank_service.transfer(username, amount, recipient)

    def update_balance(self, username, balance):
        return self.bank_service.update_balance(username, balance)
