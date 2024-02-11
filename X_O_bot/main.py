import os
import telebot
import environs
from X_O_bot import game

env = environs.Env()
env.read_env('.env')
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
CURRENT_PALYER = ['X']


def change_current_palayer(current_player):
    if current_player[0] == 'X':
        current_player[0] = 'O'
    else:
        current_player[0] = 'X'


@bot.message_handler(commands=['start'])
def start(message):
    game.clear_data()
    bot.send_message(message.chat.id, f"Новая игра началась!\n\nВаш ход: {CURRENT_PALYER[0]}\n\n{game.print_game_field()}")


@bot.message_handler(func=lambda message: message.text == 'print')
def start(message):
    bot.send_message(message.chat.id, game.print_game_field())


@bot.message_handler(content_types=['text'])
def print_game_field(message):
    if len(message.text) < 3 or len(message.text) >= 4:
        bot.send_message(message.chat.id, f"[?] Неверный формат ввода: {message.text}")
        return
    if message.text[2] != CURRENT_PALYER[0]:
        mess = f'Вы потеряли ход! Сейчас должен был ходить {CURRENT_PALYER[0]}, вы ввели {message.text[2]}\n\n'
        change_current_palayer(CURRENT_PALYER)
        bot.send_message(message.chat.id, f'{mess}Ваш ход: {CURRENT_PALYER[0]}\n\n{game.print_game_field()}')
        return
    inp_val = game.input_value(message.text[:2], message.text[2])
    is_win = game.check_is_game_end()
    if '[?]' in inp_val:
        bot.send_message(message.chat.id, inp_val)
        change_current_palayer(CURRENT_PALYER)
        return
    if is_win != 'игра прдолжается!':
        bot.send_message(message.chat.id, f'Победил: {is_win}')
        game.clear_data()
        return
    change_current_palayer(CURRENT_PALYER)
    bot.send_message(message.chat.id, f"Ваш ход: {CURRENT_PALYER[0]}\n\n{game.print_game_field()}")


bot.infinity_polling()
