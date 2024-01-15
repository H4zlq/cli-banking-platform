from databases.database import Database


class BankService(Database):
    def get_balance(self, username):
        try:
            connection = self.get_connection()

            with self.get_cursor() as cursor:
                # Get balance
                cursor.execute(
                    "SELECT balance FROM users WHERE username = %s", (username,)
                )

                # Fetch balance from database
                result = cursor.fetchone()

                # Get balance from dictionary
                balance = result["balance"]

            # Return balance as float
            return float(balance)
        except Exception as err:
            print(f"Cannot get balance: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_balance(self, username, balance):
        try:
            connection = self.get_connection()

            with self.get_cursor() as cursor:
                # Update balance
                cursor.execute(
                    "UPDATE users SET balance = %s WHERE username = %s",
                    (balance, username),
                )

            connection.commit()
        except Exception as err:
            print(f"Cannot update balance: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def deposit(self, username, amount):
        try:
            balance = self.get_balance(username)

            if amount == 0:
                print("Cannot deposit zero")
                return

            if amount < 0:
                print("Invalid amount")
                return

            # Add balance
            balance += amount

            # Update balance in database
            self.update_balance(username, balance)

            return balance
        except Exception as err:
            print(f"Cannot deposit: {err}")

    def withdraw(self, username, amount):
        try:
            balance = self.get_balance(username)

            if amount == 0:
                print("Cannot withdraw zero")
                return

            if amount < 0:
                print("Invalid amount")
                return

            # Check if balance is enough
            if balance < amount:
                print("Insufficient balance")
                return

            # Subtract balance
            balance -= amount

            # Update balance in database
            self.update_balance(username, balance)

            return balance
        except Exception as err:
            print(f"Cannot withdraw: {err}")

    def transfer(self, username, amount, recipient):
        try:
            balance = self.get_balance(username)

            if amount == 0:
                print("Cannot transfer zero")
                return

            if amount < 0:
                print("Invalid amount")
                return

            if balance < amount:
                print("Insufficient balance")
                return

            # Subtract balance
            balance -= amount

            # Update balance in database
            self.update_balance(username, balance)

            # Get recipient balance from database
            recipient_balance = self.get_balance(recipient)

            # Check if recipient exists
            if not recipient_balance:
                print("Recipient does not exist")
                return

            # Add balance
            recipient_balance += amount

            # Update balance in database
            self.update_balance(recipient, recipient_balance)

            return balance
        except Exception as err:
            print(f"Cannot transfer: {err}")
