from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.filters import CommandStart
from environs import Env

env = Env()
env.read_env()

bot = Bot(token=env('BOT_TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def process_start_button(message: Message):
    print(message.from_user.id)
    # Создаем объекты инлайн-кнопок
    big_button_1 = InlineKeyboardButton(
        text='БОЛЬШАЯ КНОПКА 1',
        callback_data='big_button_1_pressed'
    )

    big_button_2 = InlineKeyboardButton(
        text='БОЛЬШАЯ КНОПКА 2',
        callback_data='big_button_2_pressed'
    )

    # Создаем объект инлайн-клавиатуры
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[big_button_1],
                         [big_button_2]]
    )
    await message.answer(
        text='abc',
        reply_markup=keyboard
    )

@dp.callback_query(F.data == 'big_button_1_pressed')
async def process_buttons_1_press(callback: CallbackQuery):
    print(callback.message)
    await callback.message.edit_text(
        text=f'Нажата {callback.data}',
        reply_markup=callback.message.reply_markup
    )


@dp.callback_query(F.data == 'big_button_2_pressed')
async def process_buttons_2_press(callback: CallbackQuery):
    print(callback.message)
    await callback.message.edit_text(
        text=f'Нажата {callback.data}',
        reply_markup=callback.message.reply_markup
    )
dp.run_polling(bot)