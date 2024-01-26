# модуль для хранения хэндлера, который будет обрабатывать сообщения,
# не предусмотренные в рамках общения пользователя с ботом
from aiogram.types import Message
from aiogram import Router
from ..lexicon import lexicon_ru


router = Router()
@router.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=lexicon_ru.LEXICON_RU['no_echo'])
