from global_data import BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram import F
from random import randint

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class Gamer:
    def __init__(self, name:str, score:int,  isgame:bool):
        self.name = name
        self.score = score
        self.bot_number = randint(101)
        self.user_number = None
        self.isgame = isgame


@dp.message(Command(commands=['start']))
async def start(message:Message):
    gamer = Gamer(message.from_user.username, 0, True)
    await message.reply(text=f"Let's starts!!!\nYour gamedata:\n   Name: {gamer.name}\n   Score: {gamer.score}.")


@dp.message()
async def start(message:Message):
    await message.send_copy(chat_id=message.chat.id)


if __name__ == '__main__':
    dp.run_polling(bot)