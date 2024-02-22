import requests
import json
import csv
import sqlite3

from bs4 import BeautifulSoup
from datetime import datetime



class ParserMebel:
    data = None

    def __init__(self, url):
        self.url = url

    def get_data_from_url(self):
        self.data = []
        response = requests.get(self.url).text
        soup = BeautifulSoup(response, 'html.parser')
        links = soup.find_all('a', class_='styles_wrapper__5FoK7')
        for link in links:
            data = link.text.split(' р.')
            try:
                price, description = data
                price = price.replace(' ', '')
            except:
                price = 0
                description = data[0]

            self.data.append(
                {
                    'LINK': link['href'],
                    'PRICE': price,
                    'DESCRIPTION': description
                }
            )



    def write_to_csv(self):
        with open(f'{datetime.now().strftime(r"%d-%m-%Y %H.%M")} kufar_mebel', 'w', encoding='utf-8-sig',
                  newline='') as f:
            writer = csv.DictWriter(f, fieldnames=('LINK', 'PRICE', 'DESCRIPTION'), delimiter=';')
            writer.writeheader()
            for item in self.data:
                writer.writerow(item)

    def onnect_to_db(self):
        try:
            connection = sqlite3.connect("kufar.db")
        except:
            connection = False

        return connection


    def close_connection_db(self, connection):
        if connection:
            connection.close()

    def create_table_db(self, connection):
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS mebel (id INTEGER PRIMARY KEY AUTOINCREMENT, link text, price INTEGER, description text)")
            connection.commit()
        else:
            print(connection, 'ERROR CONNECTION TO DB!')
    def insert_to_db(self, connection):
        if connection:
            cursor = connection.cursor()
            for item in mebel.data:
                link, price, description = item.values()
                cursor.execute(f'INSERT INTO mebel (link, price, description) VALUES ("{link}", "{price}", "{description}")')
            connection.commit()
        else:
            print(connection, 'ERROR CONNECTION TO DB!')

    def clear_self_data(self):
        self.data.clear()



url = 'https://www.kufar.by/l/mebel'
#
mebel = ParserMebel(url)

mebel.get_data_from_url()
mebel.write_to_csv()
connection_to_db = mebel.connect_to_db()
mebel.create_table_db(connection_to_db)
mebel.insert_to_db(connection_to_db)
mebel.close_connection_db(connection_to_db)
mebel.clear_self_data()



