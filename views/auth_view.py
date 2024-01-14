from controllers.database_controller import DatabaseController
from models.user_model import UserModel
from utils.bcrypt_util import BcryptUtil


class AuthView:
    database_controller = DatabaseController()
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

                initial_balance = 0

                # Get user model
                user_model = UserModel(username, password, initial_balance)

                # Insert user
                self.database_controller.insert_user(user_model)

                print("Successfully registered")
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
                    user_model = UserModel(user[1], user[2], user[3])

                    # Get user model properties
                    password_from_model = user_model.get_password()

                    # Hash password
                    password_matched = BcryptUtil.check_password(
                        password, password_from_model.encode("utf-8")
                    )

                    # Check if password matches
                    if password_matched:
                        print(f"Welcome back {username}")

                        # Run bank view
                        chooser_view.bank_menu(username)
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
