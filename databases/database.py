import mysql.connector
from meta.singleton_meta import SingletonMeta
from utils.file_util import FileUtil
from constants.constant import init_script


class Database(metaclass=SingletonMeta):
    _connection = None

    def get_connection(self):
        try:
            self._connection = mysql.connector.connect(
                host="localhost", user="root", password="admin", database="python_bank"
            )

            return self._connection
        except mysql.connector.Error as err:
            print(f"Cannot connect to database: {err}")

        return None

    def get_cursor(self):
        return self._connection.cursor(prepared=True, dictionary=True)

    def commit(self):
        self._connection.commit()

    def init(self):
        try:
            connection = mysql.connector.connect(
                host="localhost", user="root", password="admin"
            )

            with connection.cursor() as cursor:
                # Read sql file
                sql_file = FileUtil.read_file(init_script)

                # Split the sql file into individual statements
                splitted_file = sql_file.split(";")

                for sql in splitted_file:
                    cursor.execute(sql)

            connection.commit()
        except mysql.connector.Error as err:
            print(f"Cannot initialize database: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
