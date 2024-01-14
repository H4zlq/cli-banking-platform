import time
from constants.constant import user_menu_table, bank_table
from controllers.database_controller import DatabaseController
from controllers.session_controller import SessionController
from enums.transaction_type_enum import TransactionType
from models.transaction_model import TransactionModel
from views.auth_view import AuthView


class ChooserView:
    database_controller = DatabaseController()
    session_controller = SessionController()
    auth_view = AuthView()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def main_menu(self):
        print("\n--- Welcome to Bank System ---")

        for column in user_menu_table:
            print(f"{column[0]}. {column[1]}")

        # Get user input
        user_input = input("Please choose an option: ")

        # Check if user input is valid
        if user_input not in ["1", "2", "3", "4"]:
            print("Invalid option")
            return

        # Check if user input is 1
        if user_input == "1":
            self.auth_view.login(self)
            pass

        # Check if user input is 2
        if user_input == "2":
            self.auth_view.register()
            pass

        # Check if user input is 3
        if user_input == "3":
            self.database_controller.forgot_password()
            pass

        # Check if user input is 4
        if user_input == "4":
            print("Thank you for using our system")
            exit()

        return user_input

    def bank_menu(self):
        print("\n--- Bank ---")

        # Get user session
        session = self.session_controller.get_session()

        # Get session model
        id = session.get_id()
        username = session.get_username()

        for column in bank_table:
            print(f"{column[0]}. {column[1]}")

        # Get user input
        user_input = input("Please choose an option: ")

        # Check if user input is valid
        if user_input not in ["1", "2", "3", "4", "5", "6"]:
            print("Invalid option")
            return

        # Check if user input is 1
        if user_input == "1":
            balance = self.database_controller.get_balance(username)

            print(f"Your account balance is {str(balance[0])}")
            pass

        # Check if user input is 2
        if user_input == "2":
            balance = float(input("Please enter the amount you want to deposit: "))

            if balance < 0:
                print("Invalid amount")
                return

            # Update balance
            deposited_balance = self.database_controller.deposit(username, balance)

            # Insert logs
            self.database_controller.insert_logs(
                id,
                "deposit",
                self.timestamp,
            )

            # Get transaction type
            transaction_type = TransactionType.DEPOSIT

            # Get transaction model
            transaction = TransactionModel(
                id, transaction_type.value, balance, self.timestamp
            )

            # Insert transaction history
            self.database_controller.insert_transaction(transaction)

            print(f"Successfully deposited to your account: {balance}")
            print(f"Your new balance is {str(deposited_balance)}")
            pass

        # Check if user input is 3
        if user_input == "3":
            balance = float(input("Please enter the amount you want to withdraw: "))

            if balance < 0:
                print("Invalid amount")
                return

            # Update balance
            withdrawed_balance = self.database_controller.withdraw(username, balance)

            # Insert logs
            self.database_controller.insert_logs(id, transaction_type.value, balance)

            # Get transaction type
            transaction_type = TransactionType.WITHDRAW

            # Get transaction model
            transaction = TransactionModel(
                id, transaction_type.value, balance, self.timestamp
            )

            # Insert transaction history
            self.database_controller.insert_transaction(transaction)

            print(f"Successfully withdrawn from your account: {balance}")
            print(f"Your new balance is {str(withdrawed_balance)}")
            pass

        # Check if user input is 4
        if user_input == "4":
            amount = float(input("Please enter the amount you want to transfer: "))

            if amount < 0:
                print("Invalid amount")
                return

            recipient = input("Please enter the recipient: ")

            # Update balance
            transferred_balance = self.database_controller.transfer(
                username, amount, recipient
            )

            # Insert logs
            self.database_controller.insert_logs(id, "transfer", amount)

            # Get transaction type
            transaction_type = TransactionType.TRANSFER

            # Get transaction model
            transaction = TransactionModel(
                id, transaction_type.value, balance, self.timestamp
            )

            # Insert transaction history
            self.database_controller.insert_transaction(transaction)

            print(f"Successfully transferred to {recipient}: {amount}")
            print(f"Your new balance is {str(transferred_balance)}")
            pass

        # Check if user input is 5
        if user_input == "5":
            transaction_history = self.database_controller.get_transaction(id)

            print("--- Transaction History ---")
            print("Transaction Type | Amount | Timestamp")
            for transaction in transaction_history:
                print(f"    {transaction[2]}      | {transaction[3]} | {transaction[4]}")

        # Check if user input is 6
        if user_input == "6":
            return self.main_menu()

        # Call bank view again
        self.bank_menu()
