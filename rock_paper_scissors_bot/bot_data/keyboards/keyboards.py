from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

button_yes = KeyboardButton(text='Да')
button_no = KeyboardButton(text='Нет')

kb_start = ReplyKeyboardMarkup(keyboard=[[button_yes, button_no]], resize_keyboard=True, one_time_keyboard=False)


button_stone = KeyboardButton(text='Камень 🌑')
button_scissors = KeyboardButton(text='Ножницы ✂️')
button_paper = KeyboardButton(text='Бумага 📜')

kb_for_game = ReplyKeyboardMarkup(keyboard=[[button_stone], [button_scissors], [button_paper]], resize_keyboard=True, one_time_keyboard=False)