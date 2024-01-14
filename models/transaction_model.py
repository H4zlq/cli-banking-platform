class Transaction:
    def __init__(self, user_id, transaction_type, amount, transaction_date):
        self._user_id = user_id
        self._transaction_type = transaction_type
        self._amount = amount
        self._transaction_date = transaction_date

    def get_user_id(self):
        return self._user_id

    def get_transaction_type(self):
        return self._transaction_type

    def get_amount(self):
        return self._amount

    def get_transaction_date(self):
        return self._transaction_date
