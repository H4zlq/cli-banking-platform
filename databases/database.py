import mysql.connector
from databases.database_meta import DatabaseMeta
from utils.file_util import FileUtil
from constants.constant import init_script


class Database(metaclass=DatabaseMeta):
    _connection = None

    def get_connection(self):
        try:
            self._connection = mysql.connector.connect(
                host="localhost", user="root", password="admin", database="python_bank"
            )

            return self._connection
        except mysql.connector.Error as err:
            print(f"Cannot connect to database: {err}")

    def get_cursor(self):
        return self._connection.cursor(prepared=True)

    def commit(self):
        self._connection.commit()

    def init(self):
        try:
            # Get connection
            connection = mysql.connector.connect(
                host="localhost", user="root", password="admin"
            )

            # Get cursor
            cursor = connection.cursor()

            # Read sql file
            sql_file = FileUtil.read_file(init_script)

            # Split the sql file into individual statements
            splitted_file = sql_file.split(";")

            # Execute each sql statement
            for sql in splitted_file:
                cursor.execute(sql)

            # Commit changes
            connection.commit()

            # Close cursor
            cursor.close()

            # Close connection
            connection.close()
        except mysql.connector.Error as err:
            print(f"Cannot initialize database: {err}")
