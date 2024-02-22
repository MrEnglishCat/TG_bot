from pprint import pprint

import requests
import csv
from abc import abstractmethod, ABC
from bs4 import BeautifulSoup
from datetime import datetime


class DataClient(ABC):
    data = None
    urls = 'https://www.kufar.by/l/mebel'

    @abstractmethod
    def connect_to_db(self):
        pass

    @abstractmethod
    def create_table_db(self, connection):
        pass

    def close_connection_db(self, connection):
        if connection:
            connection.close()

    def get_data_from_url(self):
        self.data = []
        response = requests.get(self.urls).text
        soup = BeautifulSoup(response, 'html.parser')
        links = soup.find_all('a', class_='styles_wrapper__5FoK7')
        for link in links:
            data = link.text.split(' р.')
            try:
                price, description = data
                # следующий if т к при одном из запросов в цену попала строка с текстом.
                # Пример: "Онлайн покупка1382"
                price = ''.join(char for char in price if char.isdigit())
            except:
                price = 0
                description = data[0]
            # словарь выбран для записи в csv через модуль csv объект DictWriter
            self.data.append(
                {
                    'LINK': link['href'],
                    'PRICE': price,
                    'DESCRIPTION': description
                }
            )

    def write_to_csv(self):
        # pattern = "%d-%m-%Y %H.%M"
        pattern_date = "%d-%m-%Y"
        with open(f'{datetime.now().strftime(pattern_date)} kufar_mebel.csv', 'w', encoding='utf-8-sig',
                  newline='') as f:
            writer = csv.DictWriter(f, fieldnames=('LINK', 'PRICE', 'DESCRIPTION'), delimiter=';', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for item in self.data:
                writer.writerow(item)

    @staticmethod
    def get_csv_filename():

        import os
        import re

        pattern_filename = r".+\.csv"
        list_of_files = []
        for file in os.listdir(os.curdir):
            filter_for_files = re.search(pattern_filename, file)
            if filter_for_files:
                list_of_files.append(file)

        return list_of_files

    def read_from_csv(self):
        '''
        МОДУЛЬ CSV
        :param file_name:
        :return: None
        '''
        file_name = self.get_csv_filename()
        if isinstance(file_name, list) and len(file_name) == 1:
            with open(*file_name, encoding='utf-8-sig') as from_file:
                reader = csv.DictReader(from_file, delimiter=';', quoting=csv.QUOTE_ALL)
                for num, line in enumerate(reader, 1):
                    print(f"{num}) {line.get('LINK', '[INFO] Значения в файле нет!')}\n\t\t{line.get('PRICE', '[INFO] Значения в файле нет!')}\n\t\t{line.get('DESCRIPTION', '[INFO] Значения в файле нет!')}")
            return
        print(f'Список доступных файлов: {file_name}')

    def read_from_csv_with_pandas(self):
        '''
        МОДУЛЬ Pandas
        :param file_name:
        :return: None
        '''
        import pandas
        file_name = self.get_csv_filename()
        if isinstance(file_name, list) and len(file_name) == 1:
            df = pandas.read_csv(*file_name)
            print(df.head(10))

            return
        print(f'Список доступных файлов: {file_name}')

    def insert_to_db(self, connection):
        if connection:
            cursor = connection.cursor()
            for item in self.data:
                link, price, description = item.values()
                # не придумал пока что как исделать в одну строку VALUES (), (), ()
                cursor.execute(
                    f"INSERT INTO mebel (link, price, description) VALUES ('{link}', '{price}', '{description}')")
            connection.commit()
        else:
            print(connection, 'ERROR CONNECTION TO DB!')

    def clear_self_data(self):
        self.data.clear()

    def run(self):
        self.get_data_from_url()
        self.write_to_csv()
        connection_to_db = self.connect_to_db()
        self.create_table_db(connection_to_db)
        self.insert_to_db(connection_to_db)
        self.close_connection_db(connection_to_db)
        self.clear_self_data()
#
