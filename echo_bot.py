from pprint import pprint

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from global_data import BOT_TOKEN
from aiogram import F


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )

# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    try:
        pprint(message.model_dump_json(indent=3))
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )


# Этот хэндлер будет срабатывать на отправку боту фото
@dp.message(F.content_type == ContentType.PHOTO)
async def send_photo_echo(message: Message):
    pprint(message)
    await message.reply_photo(message.photo[0].file_id)

@dp.message(F.sticker)
async def send_animation(message: Message):
    pprint(message)
    await message.reply_sticker(message.sticker.file_id)
    # await message.answer_animation(message.sticker.file_id)

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)




if __name__ == '__main__':
    dp.run_polling(bot)
