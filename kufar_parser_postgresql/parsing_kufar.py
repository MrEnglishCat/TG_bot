import re
import sqlite3
import psycopg2
from data_client import DataClient





class Parser_postgresql(DataClient):
    DB_NAME = "TEST"
    USER = "postgres"
    PASSWORD = "postgres"
    HOST = "localhost"
    PORT = "5432"
    def connect_to_db(self):
        try:
            connection = psycopg2.connect(dbname=self.DB_NAME, user=self.USER, password=self.PASSWORD, host=self.HOST,
                                          port=self.PORT)
        except:
            connection = False

        return connection

    def create_table_db(self, connection):
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS mebel (id serial PRIMARY KEY , link text, price INTEGER, description text)")
            connection.commit()
        else:
            print(connection, 'ERROR CONNECTION TO DB!')


class Parser_sqlite(DataClient):
    DB_NAME = "TEST"

    def connect_to_db(self):
        try:
            connection = sqlite3.connect("kufar.db")
        except:
            connection = False

        return connection

    def create_table_db(self, connection):
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS mebel (id INTEGER PRIMARY KEY, link text, price INTEGER, description text)")
            connection.commit()
        else:
            print(connection, 'ERROR CONNECTION TO DB!')
#
#
# mebel = Parser_postgresql()
# mebel.run()





mebel2 = Parser_sqlite()
mebel2.read_from_csv()
# mebel2.run()
