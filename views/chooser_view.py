from constants.constant import authentication_table, bank_table
from services.account_service import AccountService
from services.bank_service import BankService
from services.log_service import LogService
from services.session_service import SessionService
from services.transaction_service import TransactionService
from services.user_service import UserService
from enums.transaction_type_enum import TransactionType
from models.transaction_model import Transaction
from utils.time_util import TimeUtil
from views.authentication_view import AuthenticationView


class ChooserView:
    authentication_view = AuthenticationView()
    session_service = SessionService()
    account_service = AccountService()
    user_service = UserService()
    bank_service = BankService()
    log_service = LogService()
    transaction_service = TransactionService()
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
            self.account_service.forgot_password()
            pass

        if user_input == "4":
            print("Thank you for using our system")
            exit()

        return user_input

    def bank_menu(self):
        print("\n--- Bank ---")

        # Get session
        session = self.session_service.get_session()

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
            balance = self.bank_service.get_balance(username)

            print(f"Your account balance is {str(balance)}")
            pass

        if user_input == "2":
            balance = float(input("Please enter the amount you want to deposit: "))

            if balance < 0:
                print("Invalid amount")
                return

            # Update balance
            deposited_balance = self.bank_service.deposit(username, balance)

            # Insert logs
            self.log_service.insert_logs(
                id,
                "deposit",
                self.timestamp,
            )

            # Get transaction type
            transaction_type = TransactionType.DEPOSIT

            # Get transaction model
            transaction = Transaction(
                id, transaction_type.value, balance, self.timestamp
            )

            # Insert transaction history
            self.transaction_service.insert_transaction(transaction)

            print(f"Successfully deposited to your account: {balance}")
            print(f"Your new balance is {str(deposited_balance)}")
            pass

        if user_input == "3":
            balance = float(input("Please enter the amount you want to withdraw: "))

            if balance < 0:
                print("Invalid amount")
                return

            # Update balance
            withdrawed_balance = self.bank_service.withdraw(username, balance)

            # Insert logs
            self.log_service.insert_logs(id, transaction_type.value, balance)

            # Get transaction type
            transaction_type = TransactionType.WITHDRAWAL

            # Get transaction model
            transaction = Transaction(
                id, transaction_type.value, balance, self.timestamp
            )

            # Insert transaction history
            self.transaction_service.insert_transaction(transaction)

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
            transferred_balance = self.bank_service.transfer(
                username, amount, recipient
            )

            # Insert logs
            self.log_service.insert_logs(id, "transfer", amount)

            # Get transaction type
            transaction_type = TransactionType.TRANSFER

            # Get transaction model
            transaction = Transaction(
                id, transaction_type.value, balance, self.timestamp
            )

            # Insert transaction history
            self.transaction_service.insert_transaction(transaction)

            print(f"Successfully transferred to {recipient}: {amount}")
            print(f"Your new balance is {str(transferred_balance)}")
            pass

        if user_input == "5":
            transaction_history = self.transaction_service.get_transaction(id)

            print("--- Transaction History ---")
            print("Transaction Type | Amount | Timestamp")
            for transaction in transaction_history:
                print(
                    f"    {transaction[2]}      | {transaction[3]} | {transaction[4]}"
                )

        if user_input == "6":
            return self.main_menu()

        self.bank_menu()
