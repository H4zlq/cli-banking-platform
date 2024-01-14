from databases.database import Database


class LogService(Database):
    def insert_logs(self, user_id, action, date):
        try:
            connection = self.get_connection()

            with self.get_cursor() as cursor:
                # Insert logs
                cursor.execute(
                    "INSERT INTO logs (user_id, action, log_date) VALUES (%s, %s, %s)",
                    (user_id, action, date),
                )

            connection.commit()
        except Exception as err:
            print(f"Cannot insert logs: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_logs(self):
        try:
            connection = self.get_connection()

            with self.get_cursor() as cursor:
                # Get logs
                cursor.execute("SELECT * FROM logs")

                # Fetch logs
                logs = cursor.fetchall()

            return logs
        except Exception as err:
            print(f"Cannot get logs: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
