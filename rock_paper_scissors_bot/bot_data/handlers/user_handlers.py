# модуль с обработчиками апдейтов от пользователя, предусмотренных логикой бота
from pprint import pprint

from aiogram import F
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart, Command
from ..keyboards import keyboards
from ..lexicon import lexicon_ru
from random import choice


user = {}

router = Router()
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=lexicon_ru.LEXICON_RU['/start'],
        reply_markup=keyboards.kb_start
    )


@router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer(
        text=lexicon_ru.LEXICON_RU['/help'],

    )

@router.message(F.text == 'Да')
async def process_yes_command(message: Message):
    user.setdefault(
        message.from_user.id,
        {
            'bot_item': None,
            'user_item': None,
            'win': 0,
            'total_games': 0,
            'who_wins': None
        }
    )
    user[message.from_user.id]['bot_item'] = choice(['Камень', 'Ножницы', 'Бумага'])
    await message.answer(
        text=lexicon_ru.LEXICON_RU['yes'],
        reply_markup=keyboards.kb_for_game
    )

@router.message(F.text == 'Нет')
async def process_no_command(message: Message):
    await message.answer(
        text=lexicon_ru.LEXICON_RU['no'],
        reply_markup=keyboards.ReplyKeyboardRemove()
    )

@router.message(F.text.in_(['Камень 🌑']))
async def process_stone_command(message: Message):
    user[message.from_user.id]['user_item'] = 'Камень'
    if user[message.from_user.id]['bot_item'] == 'Ножницы':
        user[message.from_user.id]['who_wins'] = message.from_user.username
        user[message.from_user.id]['total_games'] += 1
    elif user[message.from_user.id]['bot_item'] == 'Камень':
        user[message.from_user.id]['who_wins'] = 'Ничья'
    else:
        user[message.from_user.id]['who_wins'] = 'bot'
    await message.answer(
        lexicon_ru.LEXICON_RU['answer'](user[message.from_user.id]['who_wins'], user[message.from_user.id]['bot_item'] if user[message.from_user.id]['who_wins'] == 'bot' else user[message.from_user.id]['user_item'], message.from_user.username if user[message.from_user.id]['who_wins'] == 'bot' else 'bot', user[message.from_user.id]['user_item'] if user[message.from_user.id]['who_wins'] == 'bot' else user[message.from_user.id]['bot_item']),
        reply_markup=keyboards.kb_start
    )

@router.message(F.text.in_(['Ножницы ✂️']))
async def process_scissors_command(message: Message):
    user[message.from_user.id]['user_item'] = 'Ножницы'
    if user[message.from_user.id]['bot_item'] == 'Камень':
        user[message.from_user.id]['who_wins'] = message.from_user.username
        user[message.from_user.id]['total_games'] += 1
    elif user[message.from_user.id]['bot_item'] == 'Ножницы':
        user[message.from_user.id]['who_wins'] = 'Ничья'
    else:
        user[message.from_user.id]['who_wins'] = 'bot'
    await message.answer(
        lexicon_ru.LEXICON_RU['answer'](user[message.from_user.id]['who_wins'], user[message.from_user.id]['bot_item'] if user[message.from_user.id]['who_wins'] == 'bot' else user[message.from_user.id]['user_item'], message.from_user.username if user[message.from_user.id]['who_wins'] == 'bot' else 'bot', user[message.from_user.id]['user_item'] if user[message.from_user.id]['who_wins'] == 'bot' else user[message.from_user.id]['bot_item']),
        reply_markup=keyboards.kb_start
    )

@router.message(F.text.in_(['Бумага 📜']))
async def process_paper_command(message: Message):
    user[message.from_user.id]['user_item'] = 'Бумага'
    if user[message.from_user.id]['bot_item'] == 'Камень':
        user[message.from_user.id]['who_wins'] = message.from_user.username
        user[message.from_user.id]['total_games'] += 1
    elif user[message.from_user.id]['bot_item'] == 'Бумага':
        user[message.from_user.id]['who_wins'] = 'Ничья'
    else:
        user[message.from_user.id]['who_wins'] = 'bot'
    await message.answer(
        lexicon_ru.LEXICON_RU['answer'](user[message.from_user.id]['who_wins'], user[message.from_user.id]['bot_item'] if user[message.from_user.id]['who_wins'] == 'bot' else user[message.from_user.id]['user_item'], message.from_user.username if user[message.from_user.id]['who_wins'] == 'bot' else 'bot', user[message.from_user.id]['user_item'] if user[message.from_user.id]['who_wins'] == 'bot' else user[message.from_user.id]['bot_item']),
        reply_markup=keyboards.kb_start
    )

@router.message(Command('stat'))
async def process_stat_commands(message: Message):
    pprint(user)
    await message.answer(
        text=f'Name: {message.from_user.username}\nTotal games: {user[message.from_user.id]["total_games"]}' if user and user[message.from_user.id] else 'Статистики пока что нет!'
    )