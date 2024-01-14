from databases.database import Database
from utils.util import Util


class DatabaseController(Database):
    # Account controller
    def forgot_password(self):
        print("\n--- Forgot Password ---")
        username = input("Please enter your username: ")

        try:
            user = self.get_user(username)

            if user:
                password = input("Please enter your new password: ")
                confirm_password = input("Please confirm your new password: ")

                if password != confirm_password:
                    print("Password does not match")
                    return

                # Hash password
                hashed_password = Util.hash_password(password)

                # Update password
                self.update_password(username, hashed_password)

                print("Successfully updated password")
            else:
                print("Account does not exist")
        except Exception as err:
            print(f"Cannot update password: {err}")

    def update_password(self, username, password):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Update password
            cursor.execute(
                "UPDATE users SET password = %s WHERE username = %s",
                (password, username),
            )

            # Commit changes
            connection.commit()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()
        except Exception as err:
            print(f"Cannot update password: {err}")

    # User controller
    def get_user(self, username):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Get user
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

            # Fetch user
            user = cursor.fetchone()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()

            return user
        except Exception as err:
            print(f"Cannot get user: {err}")

    def insert_user(self, user_model):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Get user model properties
            username = user_model.get_username()
            password = user_model.get_password()
            balance = user_model.get_balance()

            # Hash password
            hashed_password = Util.hash_password(password)

            # Insert user
            cursor.execute(
                "INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)",
                (username, hashed_password, balance),
            )

            # Commit changes
            connection.commit()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()
        except Exception as err:
            print(f"Cannot register user: {err}")

    # Bank controller
    def get_balance(self, username):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Get balance
            cursor.execute("SELECT balance FROM users WHERE username = %s", (username,))

            # Fetch balance
            balance = cursor.fetchone()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()

            return balance
        except Exception as err:
            print(f"Cannot get balance: {err}")

    def update_balance(self, username, balance):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Update balance
            cursor.execute(
                "UPDATE users SET balance = %s WHERE username = %s", (balance, username)
            )

            # Commit changes
            connection.commit()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()
        except Exception as err:
            print(f"Cannot update balance: {err}")

    def deposit(self, username, amount):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Get balance
            cursor.execute("SELECT balance FROM users WHERE username = %s", (username,))

            # Fetch balance
            balance = cursor.fetchone()

            # Get balance from tuple
            balance = balance[0]

            # Check if amount is zero
            if amount == 0:
                print("Cannot deposit zero")
                return

            # Check if amount is negative
            if amount < 0:
                print("Invalid amount")
                return

            # Convert to float
            balance = float(balance)

            # Add balance
            balance += amount

            # Update balance
            self.update_balance(username, balance)

            # Commit changes
            connection.commit()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()

            return balance
        except Exception as err:
            print(f"Cannot deposit: {err}")

    def withdraw(self, username, amount):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Get balance
            cursor.execute("SELECT balance FROM users WHERE username = %s", (username,))

            # Fetch balance
            balance = cursor.fetchone()

            # Get balance from tuple
            balance = balance[0]

            # Check if amount is zero
            if amount == 0:
                print("Cannot withdraw zero")
                return

            # Check if amount is negative
            if amount < 0:
                print("Invalid amount")
                return

            # Convert to float
            balance = float(balance)

            # Check if balance is enough
            if balance < amount:
                print("Insufficient balance")
                return

            # Subtract balance
            balance -= amount

            # Update balance
            self.update_balance(username, balance)

            # Commit changes
            connection.commit()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()

            return balance
        except Exception as err:
            print(f"Cannot withdraw: {err}")

    def transfer(self, username, amount, recipient):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Get balance
            cursor.execute("SELECT balance FROM users WHERE username = %s", (username,))

            # Fetch balance
            balance = cursor.fetchone()

            # Get balance from tuple
            balance = balance[0]

            # Check if amount is zero
            if amount == 0:
                print("Cannot transfer zero")
                return

            # Check if amount is negative
            if amount < 0:
                print("Invalid amount")
                return

            # Check if balance is enough
            if balance < amount:
                print("Insufficient balance")
                return

            # Convert to float
            balance = float(balance)

            # Subtract balance
            balance -= amount

            # Update balance
            self.update_balance(username, balance)

            # Get balance
            cursor.execute(
                "SELECT balance FROM users WHERE username = %s", (recipient,)
            )

            # Fetch balance
            balance = cursor.fetchone()

            # Check if recipient exists
            if not balance:
                print("Recipient does not exist")
                return

            # Get balance from tuple
            balance = balance[0]

            # Convert to float
            balance = float(balance)

            # Add balance
            balance += amount

            # Update balance
            self.update_balance(recipient, balance)

            # Commit changes
            connection.commit()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()

            return balance
        except Exception as err:
            print(f"Cannot transfer: {err}")

    # Transaction history controller
    def insert_logs(self, action, balance):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Insert logs
            cursor.execute(
                "INSERT INTO logs (action, balance) VALUES (%s, %s)",
                (action, balance),
            )

            # Commit changes
            connection.commit()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()
        except Exception as err:
            print(f"Cannot insert logs: {err}")

    def get_logs(self):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Get logs
            cursor.execute("SELECT * FROM logs")

            # Fetch logs
            logs = cursor.fetchall()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()

            return logs
        except Exception as err:
            print(f"Cannot get logs: {err}")
