from controllers.database_controller import DatabaseController
from controllers.session_controller import SessionController
from enums.account_type_enum import AccountType
from models.user_model import UserModel
from utils.bcrypt_util import BcryptUtil
from constants.constant import account_type_table


class AuthView:
    database_controller = DatabaseController()
    session_controller = SessionController()
    max_attempts = 3
    attempts = 0

    def register(self):
        print("\n--- Register ---")
        username = input("Please enter a username: ")

        try:
            user = self.database_controller.get_user(username)

            # Check if username exists
            if user:
                print(
                    "Account already exists, Please login instead of register new account."
                )
            else:
                password = input("Please enter a password: ")
                confirm_password = input("Please confirm your password: ")

                if password != confirm_password:
                    print("Password does not match")
                    return

                print("Please choose account type: ")
                for column in account_type_table:
                    print(f"{column[0]}. {column[1]}")

                # Get user input
                user_input = input("Please choose an option: ")

                # Get account type
                account_type = None
                savings = AccountType.SAVINGS
                current = AccountType.CURRENT

                # Check if user input is valid
                if user_input not in ["1", "2"]:
                    print("Invalid option")
                    return

                # Check if user input is 1
                if user_input == "1":
                    account_type = savings
                    initial_balance = 1000

                # Check if user input is 2
                if user_input == "2":
                    account_type = current
                    initial_balance = 0

                # Get user model
                user_model = UserModel(
                    username, password, account_type.value, initial_balance
                )

                # Insert user
                self.database_controller.insert_user(user_model)

                print(f"Successfully registered as {username}")
        except Exception as err:
            print(f"Cannot register user: {err}")

    def login(self, chooser_view):
        print("\n--- Login ---")
        while self.attempts < self.max_attempts:
            username = input("Please enter your username: ")

            try:
                user = self.database_controller.get_user(username)

                if user:
                    password = input("Please enter your password: ")

                    # Get user model
                    user_model = UserModel(user[0], user[1], user[2], user[3], user[4])

                    # Get user model properties
                    password_from_model = user_model.get_password()

                    # Hash password
                    password_matched = BcryptUtil.check_password(
                        password, password_from_model.encode("utf-8")
                    )

                    # Check if password matches
                    if password_matched:
                        print(f"Welcome back {username}")

                        # Create user session
                        self.session_controller.set_session(user_model)

                        # Run bank view
                        chooser_view.bank_menu()
                    else:
                        print("Invalid credentials\n")

                        if self.attempts == 3:
                            print("Too many attempts, please try again later")
                            return

                        self.attempts += 1
                else:
                    print("Account does not exist\n")
                    self.attempts += 1
            except Exception as err:
                print(f"Cannot login user: {err}")
