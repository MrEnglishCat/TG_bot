# модуль с обработчиками апдейтов от пользователя, предусмотренных логикой бота
from aiogram import F
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart

router = Router()
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Давайте начнем игру!\nЖелаете ли вы продолжить?\n\nНажмите кнопку "Да" или "Нет"'
    )
