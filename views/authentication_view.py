from controllers.account_controller import AccountController
from controllers.session_controller import SessionController
from controllers.user_controller import UserController
from enums.account_type_enum import AccountType
from models.user_model import User
from utils.bcrypt_util import BcryptUtil
from constants.constant import account_type_table


class AuthenticationView:
    account_controller = AccountController()
    user_controller = UserController()
    max_attempts = 3
    attempts = 0

    def register(self):
        print("\n--- Register ---")
        username = input("Please enter a username: ")

        try:
            user_from_database = self.user_controller.get_user(username)

            if user_from_database:
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

                user_input = input("Please choose an option: ")

                # Get account type
                account_type = None
                savings = AccountType.SAVINGS
                current = AccountType.CURRENT

                if user_input not in ["1", "2"]:
                    print("Invalid option")
                    return

                if user_input == "1":
                    account_type = savings
                    initial_balance = 1000

                if user_input == "2":
                    account_type = current
                    initial_balance = 0

                # Get user model
                user = User(-1, username, password, account_type.value, initial_balance)

                # Insert user
                self.user_controller.insert_user(user)

                print(f"Successfully registered as {username}")
        except Exception as err:
            print(f"Cannot register user: {err}")

    def login(self, chooser_view):
        session_controller = SessionController(self)

        # Check if session exists
        session = session_controller.get_session()

        if session:
            print("You are already logged in")
            chooser_view.bank_menu()
            return

        print("\n--- Login ---")
        while self.attempts < self.max_attempts:
            username = input("Please enter your username: ")

            try:
                user_from_database = self.user_controller.get_user(username)

                if user_from_database:
                    password = input("Please enter your password: ")

                    # Get user model
                    user = User(
                        user_from_database["id"],
                        user_from_database["username"],
                        user_from_database["password"],
                        user_from_database["account_type_id"],
                        user_from_database["balance"],
                    )

                    # Get hashed password from user model and database
                    hashed_password = user.get_password()

                    # Hash password
                    password_matched = BcryptUtil.check_password(
                        password, hashed_password.encode("utf-8")
                    )

                    if password_matched:
                        print(f"Welcome back {username}")

                        # Create user session
                        session_controller.start_session(user)

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

    def forgot_password(self):
        print("\n--- Forgot Password ---")
        username = input("Please enter your username: ")

        try:
            user_from_database = self.user_controller.get_user(username)

            if user_from_database:
                current_password = input("Please enter your current password: ")
                password = input("Please enter your new password: ")
                confirm_password = input("Please confirm your new password: ")

                if current_password != user_from_database["password"]:
                    print("Current password does not match")
                    return

                if password != confirm_password:
                    print("Password does not match")
                    return

                # Hash password
                hashed_password = BcryptUtil.hash_password(password)

                self.account_controller.update_password(username, hashed_password)

                print("Successfully updated password")
            else:
                print("Account does not exist")
        except Exception as err:
            print(f"Cannot update password: {err}")
