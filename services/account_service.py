from databases.database import Database
from utils.bcrypt_util import BcryptUtil


class AccountService(Database):
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
                hashed_password = BcryptUtil.hash_password(password)

                self.update_password(username, hashed_password)

                print("Successfully updated password")
            else:
                print("Account does not exist")
        except Exception as err:
            print(f"Cannot update password: {err}")

    def update_password(self, username, password):
        try:
            connection = self.get_connection()

            with self.get_cursor() as cursor:
                # Update password
                cursor.execute(
                    "UPDATE users SET password = %s WHERE username = %s",
                    (password, username),
                )

            connection.commit()
        except Exception as err:
            print(f"Cannot update password: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
