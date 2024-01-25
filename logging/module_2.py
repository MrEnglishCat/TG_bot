import logging

logger = logging.getLogger(__name__)

from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    db_host: str       # URL-адрес базы данных
    db_user: str       # Username пользователя базы данных
    db_password: str   # Пароль к базе данных
    database: str      # Название базы данных


@dataclass
class TgBot:
    token: str             # Токен для доступа к телеграм-боту
    admin_ids: list[int]   # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
def devide_number(dividend: int | float, devider: int | float):

    logger.debug('Лог DEBUG')
    logger.info('Лог INFO')
    logger.warning('Лог WARNING')
    logger.error('Лог ERROR')
    logger.critical(f'Лог CRITICAL')

    try:
        return dividend / devider
    except ZeroDivisionError:
        logger.exception('Произошло деление на 0')