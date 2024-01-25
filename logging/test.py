import sys

from aiogram.filters import ChatMemberUpdatedFilter, KICKED
from aiogram.types import ChatMemberUpdated

from aiogram import F

import logging

# Определяем свой фильтр, наследуюясь от класса Filter библиотеки logging
class ErrorLogFilter(logging.Filter):
    # Переопределяем метод filter, который принимает `self` и `record`
    # Переменная рекорд будет ссылаться на объект класса LogRecord
    def filter(self, record):
        return record.levelname == 'ERROR' and 'важно' in record.msg.lower()

format_txt = '[{asctime}] #{levelname:8} ---- {filename}:{lineno} ---- {name} ---- {message}'
format_csv = '[{asctime}];#{levelname:8};{filename}:{lineno};{name};{message}'

logger_1 = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
formatter_txt = logging.Formatter(fmt=format_txt, style='{')
formatter_csv = logging.Formatter(fmt=format_csv, style='{')
file_txt_handler = logging.FileHandler('log.txt', mode='a')
file_csv_handler = logging.FileHandler('log.csv', mode='a')
file_txt_handler.setFormatter(formatter_txt)
file_csv_handler.setFormatter(formatter_csv)
logger_1.addHandler(file_txt_handler)
logger_1.addHandler(file_csv_handler)
logger_1.addFilter(ErrorLogFilter())
logger_1.debug('asdasasdasdad')
logger_1.warning('asdasasdasdad')
logger_1.setLevel('DEBUG')
logger_1.debug('===asdasasdasdad')
logger_1.warning('===asdasasdasdad')
