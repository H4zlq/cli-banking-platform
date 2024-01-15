from constants.constant import authentication_table, bank_table
from controllers.bank_controller import BankController
from controllers.log_controller import LogController
from controllers.session_controller import SessionController
from controllers.transaction_controller import TransactionController
from enums.transaction_type_enum import TransactionType
from models.transaction_model import Transaction
from utils.time_util import TimeUtil
from views.authentication_view import AuthenticationView


class ChooserView:
    authentication_view = AuthenticationView()
    session_controller = SessionController()
    bank_controller = BankController()
    log_controller = LogController()
    transaction_controller = TransactionController()
    timestamp = TimeUtil.get_timestamp()

    def main_menu(self):
        print("\n--- Welcome to Bank System ---")

        for column in authentication_table:
            print(f"{column[0]}. {column[1]}")

        user_input = input("Please choose an option: ")

        if user_input not in ["1", "2", "3", "4"]:
            print("Invalid option")
            return

        if user_input == "1":
            self.authentication_view.login(self)
            pass

        if user_input == "2":
            self.authentication_view.register()
            pass

        if user_input == "3":
            self.authentication_view.forgot_password()
            pass

        if user_input == "4":
            print("Thank you for using our system")
            exit()

        return user_input

    def bank_menu(self):
        print("\n--- Bank ---")

        # Get session
        session = self.session_controller.get_session()

        # Get session model
        id = session.get_id()
        username = session.get_username()

        for column in bank_table:
            print(f"{column[0]}. {column[1]}")

        user_input = input("Please choose an option: ")

        if user_input not in ["1", "2", "3", "4", "5", "6"]:
            print("Invalid option")
            return

        if user_input == "1":
            balance = self.bank_controller.get_balance(username)
            print(f"Your current balance is {str(balance)}")
            pass

        if user_input == "2":
            balance = float(input("Please enter the amount you want to deposit: "))

            if balance < 0:
                print("Invalid amount")
                return

            # Update balance
            deposited_balance = self.bank_controller.deposit(username, balance)

            # Get transaction type
            transaction_type = TransactionType.DEPOSIT

            # Insert logs and transaction
            self.insert_logs_and_transaction(
                id, transaction_type, balance, self.timestamp
            )

            print(f"Successfully deposited to your account: {balance}")
            print(f"Your new balance is {str(deposited_balance)}")
            pass

        if user_input == "3":
            balance = float(input("Please enter the amount you want to withdraw: "))

            if balance < 0:
                print("Invalid amount")
                return

            # Update balance
            withdrawed_balance = self.bank_controller.withdraw(username, balance)

            # Get transaction type
            transaction_type = TransactionType.WITHDRAWAL

            # Insert logs and transaction
            self.insert_logs_and_transaction(
                id, transaction_type, balance, self.timestamp
            )

            print(f"Successfully withdrawn from your account: {balance}")
            print(f"Your new balance is {str(withdrawed_balance)}")
            pass

        if user_input == "4":
            amount = float(input("Please enter the amount you want to transfer: "))

            if amount < 0:
                print("Invalid amount")
                return

            recipient = input("Please enter the recipient: ")

            # Update balance
            transferred_balance = self.bank_controller.transfer(
                username, amount, recipient
            )

            # Get transaction type
            transaction_type = TransactionType.TRANSFER

            # Insert logs and transaction
            self.insert_logs_and_transaction(
                id, transaction_type, amount, self.timestamp
            )

            print(f"Successfully transferred to {recipient}: {amount}")
            print(f"Your new balance is {str(transferred_balance)}")
            pass

        if user_input == "5":
            transaction_history = self.transaction_controller.get_transactions(id)
            pass

            print("--- Transaction History ---")
            print(
                "{:<20} | {:<10} | {:<20}".format(
                    "Transaction Type", "Amount", "Transaction Date"
                )
            )
            for transaction in transaction_history:
                transaction = Transaction(
                    transaction["user_id"],
                    transaction["transaction_type"],
                    transaction["amount"],
                    transaction["transaction_date"],
                )

            transaction_type = transaction.get_transaction_type()
            amount = transaction.get_amount()
            transaction_date = transaction.get_transaction_date()
            print(type(transaction_date))

            print(
                "{:<20} | {:<10} | {:<20}".format(
                    transaction_type, str(amount), str(transaction_date)
                )
            )

        if user_input == "6":
            return self.main_menu()

        self.bank_menu()

    def insert_logs_and_transaction(self, id, transaction_type, amount, date):
        # Insert logs
        self.log_controller.insert_logs(id, transaction_type.value, date)

        transaction = Transaction(id, transaction_type.value, amount, date)

        self.transaction_controller.insert_transaction(transaction)
