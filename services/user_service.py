from databases.database import Database
from utils.bcrypt_util import BcryptUtil


class UserService(Database):
    def get_user(self, username):
        try:
            connection = self.get_connection()

            with self.get_cursor() as cursor:
                # Get user
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

                # Fetch user
                result = cursor.fetchone()

            return result
        except Exception as err:
            print(f"Cannot get user: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def insert_user(self, user):
        try:
            connection = self.get_connection()

            # Get user model properties
            username = user.get_username()
            password = user.get_password()
            account_type_id = user.get_account_type_id()
            balance = user.get_balance()

            # Hash password
            hashed_password = BcryptUtil.hash_password(password)

            with self.get_cursor() as cursor:
                # Insert user
                cursor.execute(
                    "INSERT INTO users (username, password, account_type_id, balance) VALUES (%s, %s, %s, %s)",
                    (username, hashed_password, account_type_id, balance),
                )

            connection.commit()
        except Exception as err:
            print(f"Cannot register user: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
