import os
import telebot
import environs
from X_O_bot import game

env = environs.Env()
env.read_env('.env')
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))



@bot.message_handler(commands=['start'])
def start(message):
	game.clear_data()
	bot.reply_to(message, f"Новая игра началась!\n\n{game.print_game_field()}")

@bot.message_handler(func=lambda message: message.text == 'print')
def start(message):
	bot.reply_to(message, game.print_game_field())



@bot.message_handler(content_types=['text'])
def print_game_field(message):
	if len(message.text) < 3:
		bot.reply_to(message, f"[?] Неверный формат ввода: {message.text}")
		return
	inp_val = game.input_value(message.text[:2], message.text[2])
	is_win = game.check_is_game_end()
	if '[?]' in inp_val:
		bot.reply_to(message, inp_val)
		return
	print(inp_val, is_win)
	if is_win != 'игра прдолжается!':
		print(f'Победил: {is_win}')
		bot.reply_to(message, f'Победил: {is_win}')
		game.clear_data()
		return

	bot.reply_to(message, game.print_game_field())




bot.infinity_polling()
