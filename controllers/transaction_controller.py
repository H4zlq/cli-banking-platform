from enums.transaction_type_enum import TransactionType
from models.transaction_model import Transaction
from services.transaction_service import TransactionService


class TransactionController:
    transaction_service = TransactionService()

    def get_transactions(self):
        return self.transaction_service.get_transactions()

    def insert_transactions(self, transaction):
        return self.transaction_service.insert_transaction(transaction)
