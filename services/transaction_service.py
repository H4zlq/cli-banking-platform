from databases.database import Database


class TransactionService(Database):
    def insert_transaction(self, transaction):
        try:
            connection = self.get_connection()

            with self.get_cursor() as cursor:
                # Get transaction properties
                user_id = transaction.get_user_id()
                transaction_type = transaction.get_transaction_type()
                amount = transaction.get_amount()
                transaction_date = transaction.get_transaction_date()

                # Insert transaction
                cursor.execute(
                    "INSERT INTO transactions (user_id, transaction_type, amount, transaction_date) VALUES (%s, %s, %s, %s)",
                    (user_id, transaction_type, amount, transaction_date),
                )

            connection.commit()
        except Exception as err:
            print(f"Cannot insert transaction: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_transaction(self, user_id):
        try:
            connection = self.get_connection()

            with self.get_cursor() as cursor:
                # Get transactions
                cursor.execute(
                    "SELECT * FROM transactions WHERE user_id = %s", (user_id,)
                )

                # Fetch transactions
                transactions = cursor.fetchall()

            return transactions
        except Exception as err:
            print(f"Cannot get transaction: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
