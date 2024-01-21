from global_data import BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram import F

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def start(message:Message):
    await message.reply(text="Let's starts!!!")


# @dp.message()
# async def start(message:Message):
#     await message.send_copy(chat_id=message.chat.id)
#

if __name__ == '__main__':
    dp.run_polling(bot)