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
            if len(data) > 1:
                price, description = data
                price = price.replace(' ', '')
            else:
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

        self.data.clear()


url = 'https://www.kufar.by/l/mebel'
#
mebel = ParserMebel(url)
mebel.get_data_from_url()
# mebel.write_to_csv()



connection = sqlite3.connect("kufar.db")


cursor = connection.cursor()
# cursor.execute('DROP TABLE mebel')
cursor.execute(f"CREATE TABLE IF NOT EXISTS mebel (id INTEGER PRIMARY KEY AUTOINCREMENT, link text, price INTEGER, description text)")
for item in mebel.data:
    link, price, description = item.values()
    cursor.execute(f'INSERT INTO mebel (link, price, description) VALUES ("{link}", "{price}", "{description}")')
connection.commit()
cursor.execute(f"SELECT * FROM mebel WHERE price = 0")


result = cursor.fetchall()
connection.close()
print(*result, sep='\n')