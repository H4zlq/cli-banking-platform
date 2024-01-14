import mysql.connector
from databases.database_meta import DatabaseMeta
from utils.file_util import FileUtil


class Database(metaclass=DatabaseMeta):
    _connection = None

    def get_connection(self):
        try:
            self._connection = mysql.connector.connect(
                host="localhost", user="root", password="admin", database="bank_system"
            )

            return self._connection
        except mysql.connector.Error as err:
            print(f"Cannot connect to database: {err}")

    def get_cursor(self):
        return self._connection.cursor()

    def commit(self):
        self._connection.commit()

    def init(self):
        try:
            # Get connection
            connection = self.get_connection()

            # Get cursor
            cursor = self.get_cursor()

            # Read sql file
            sql_file = FileUtil.read_file("scripts/init.sql")

            # Split the sql file into individual statements
            splitted_file = sql_file.split(";")

            # Execute each sql statement
            for sql in splitted_file:
                cursor.execute(sql)

            # Commit changes
            connection.commit()

            # Close cursor
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Cannot initialize database: {err}")
