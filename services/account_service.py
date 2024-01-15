from databases.database import Database


class AccountService(Database):
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
