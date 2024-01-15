from services.transaction_service import TransactionService


class TransactionController:
    transaction_service = TransactionService()

    def get_transactions(self, user_id):
        return self.transaction_service.get_transactions(user_id)

    def insert_transaction(self, transaction):
        return self.transaction_service.insert_transaction(transaction)
