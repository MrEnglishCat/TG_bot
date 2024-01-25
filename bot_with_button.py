from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

from environs import Env
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import random


kb_builder = ReplyKeyboardBuilder()
env = Env()
env.read_env()
user = {
    'bot_item': None,
    'user_item': None,
    'win': None
}

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = env('BOT_TOKEN')

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем объекты кнопок
game_button_1 = KeyboardButton(text='Камень 🌑')
game_button_2 = KeyboardButton(text='Ножницы ✂️')
game_button_3 = KeyboardButton(text='Бумага 📜')
button_yes = KeyboardButton(text='Да')
button_no = KeyboardButton(text='Нет')



kb_builder.row(*[game_button_1, game_button_2, game_button_3])

# Создаем объект клавиатуры, добавляя в него кнопки

kb_start = ReplyKeyboardMarkup(keyboard=[[button_yes, button_no]], resize_keyboard=True)
keyboard = ReplyKeyboardMarkup(
    keyboard=[[game_button_1, game_button_2]],
    resize_keyboard=True,
    # one_time_keyboard=True
)

def _check_data(user, bot):
    if user == 'Камень 🌑' and bot == 'Ножницы ✂️':
        return 'user'
    else:
        return 'bot'
# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@dp.message(CommandStart())
async def process_start_command(message: Message):

    await message.answer(
        text=f'Приветствую, {message.from_user.username}!\nЖелаешь ли ты сыграть в игру "Камень, ножницы, бумага"?',
        reply_markup=kb_start
    )

@dp.message(F.text == 'Да')
async def process_yes_game(message: Message):
    user['bot_item'] = random.choice(['Камень 🌑', 'Ножницы ✂️', 'Бумага 📜'])
    await  message.answer(
        text='Отлично!\nЯ свой вариант выбрал!\nТеперь выбирайте вы! =)',
        reply_markup=kb_builder.as_markup(resize_keyboard=True)
    )

@dp.message(F.text == 'Нет')
async def process_yes_game(message: Message):
    await  message.answer(
        text='Отлично!\nХорошего дня!\nЗаходите позже! =)',
        reply_markup=ReplyKeyboardRemove()
    )


# Этот хэндлер будет срабатывать на ответ "Собак 🦮" и удалять клавиатуру
@dp.message(F.text == 'Камень 🌑')
async def process_dog_answer(message: Message):
    user['user_item'] = message.text
    if _check_data(user['user_item'], user['bot_item']) == 'user':
        user['win'] = message.from_user.username
    else:
        user['win'] = 'bot'
    await message.answer(
        text=f'Победил {user["win"]}!\nЖелаете сыграть еще раз?',
        reply_markup=kb_start
    )


# Этот хэндлер будет срабатывать на ответ "Огурцов 🥒" и удалять клавиатуру
@dp.message(F.text == 'Ножницы ✂️')
async def process_cucumber_answer(message: Message):
    await message.answer(
        text='Ножницы ✂️',
        # reply_markup=ReplyKeyboardRemove()
    )


@dp.message(F.text == 'Бумага 📜')
async def process_cucumber_answer(message: Message):
    await message.answer(
        text='Бумага 📜',
        # reply_markup=ReplyKeyboardRemove()
    )


if __name__ == '__main__':
    dp.run_polling(bot)