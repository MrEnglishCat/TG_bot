import json
import random

# from global_data import BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ContentType
from aiogram import F
from random import randint
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

class User:
    def __init__(self, used_id=None, in_game:bool=False, secret_number:int=None, attempts:int=None, total_games:int=0, wins:int=0):
        self.user_id = used_id
        self.in_game = in_game
        self.secret_number = secret_number
        self.attempts = attempts
        self.total_games = total_games
        self.wins = wins

    def reset_attrs(self):
        self.in_game = False
        self.secret_number = None
        self.attempts = None
        self.total_games = 0
        self.wins = 0

    def __repr__(self):
        return f'User(user_id={self.user_id}, in_game={self.in_game}, secret_number={self.secret_number}, attempts={self.attempts}, total_games={self.total_games}, wins={self.wins})'


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5

user = {}

def comparator(item):
    return isinstance(item, int) and not item // 7

def custom_filter(some_list:list):
    return sum(filter(lambda item: isinstance(item, int) and not item // 7, some_list)) > 83


def get_random_number():
    return random.randint(1, 100)

@dp.message(CommandStart())
async def start(message:Message):
    await message.reply(text=f"Давайте начнем! Хотите сыграть в игру?")

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )

@dp.message(Command(commands='stat'))
async def process_stat_command(message:Message):
    if user:
        await message.answer(
            f'ID игрока: {message.from_user.id}\n'
            f'Текущее имя игрока: {message.from_user.username}\n'
            f'Всего игр сыграно: {user[message.from_user.id].total_games}\n'
            f'Игр выиграно: {user[message.from_user.id].wins}'
        )
    else:
        await message.answer(
            f'Статистика пуста!'
        )

# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if user[message.from_user.id].in_game:
        user[message.from_user.id].in_game = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы итак с вами не играем. '
            'Может, сыграем разок?'
        )

# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть', 'еще', 'ещё']))
async def process_positive_answer(message: Message):
    if not message.from_user.id in user:
        user.setdefault(message.from_user.id, User())
        user[message.from_user.id].user_id = message.from_user.id
    if not user[message.from_user.id].in_game:
        user[message.from_user.id].in_game = True
        user[message.from_user.id].secret_number = get_random_number()
        user[message.from_user.id].attempts = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user[message.from_user.id].in_game:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if user[message.from_user.id].in_game:
        if int(message.text) < user[message.from_user.id].secret_number:
            user[message.from_user.id].attempts -= 1

            await message.reply(f"Вы выбрали число меньше чем я загадал!\nОсталось попыток: {user[message.from_user.id].attempts}")
        elif int(message.text) > user[message.from_user.id].secret_number:
            user[message.from_user.id].attempts -= 1

            await message.reply(f"Вы выбрали число больше чем я загадал!\nОсталось попыток: {user[message.from_user.id].attempts} ")
        else:
            user[message.from_user.id].in_game = False

            user[message.from_user.id].wins += 1
            user[message.from_user.id].attempts = ATTEMPTS
            user[message.from_user.id].total_games += 1
            await message.reply(f"Вы победили! Было загадано {user[message.from_user.id].secret_number}\nХотите сыграть ещё?")
    else:
        await message.reply(f"Мы еще не играем. Хотите сыграть?")

    if not user[message.from_user.id].attempts:
        user[message.from_user.id].in_game = False
        user[message.from_user.id].attempts = ATTEMPTS
        user[message.from_user.id].total_games += 1
        await message.reply(f"Игра завершена\nХотите сыграть ещё?")

@dp.message(Command(commands='get_dict'))
async def get_dict(message:Message):
    await message.reply(f"{repr(user[message.from_user.id]) if user else 'Игроков не найдено!!! =('}")

@dp.message()
async def start(message:Message):
    await message.reply(f"Я могу только играть в числа! =)")


if __name__ == '__main__':
    dp.run_polling(bot)