# модуль для хранения хэндлера, который будет обрабатывать сообщения,
# не предусмотренные в рамках общения пользователя с ботом
from aiogram.types import Message
from aiogram import Router

router = Router()
@router.message()
async def process_start_command(message: Message):
    await message.answer(
        text='Управление мной работает только посредством кнопок! ;)'
    )
