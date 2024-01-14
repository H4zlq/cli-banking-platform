from constants.constant import user_menu_table, bank_table
from controllers.database_controller import DatabaseController
from views.auth_view import AuthView


class ChooserView:
    database_controller = DatabaseController()
    auth_view = AuthView()

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

    def bank_menu(self, username):
        print("\n--- Bank ---")
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

            # Insert transaction history
            self.database_controller.insert_logs("deposit", balance)

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

            # Insert transaction history
            self.database_controller.insert_logs("withdraw", balance)

            print(f"Successfully withdrawn to your account: {balance}")
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

            # Insert transaction history
            self.database_controller.insert_logs("transfer", amount)

            print(f"Successfully transferred to {recipient}: {amount}")
            print(f"Your new balance is {str(transferred_balance)}")
            pass

        # Check if user input is 5
        if user_input == "5":
            transaction_history = self.database_controller.get_logs()

            print("--- Transaction History ---")
            print("Action | Amount")
            for transaction in transaction_history:
                print(f"{transaction[1]} | {str(transaction[2])}")
            pass

        # Check if user input is 6
        if user_input == "6":
            return self.main_menu()

        # Call bank view again
        self.bank_menu(username)
