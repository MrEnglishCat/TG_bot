#encoding=utf-8-sig
from pprint import pprint
import random
import requests
import time
# from global_data import BOT_TOKEN
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

API_URL = 'https://api.telegram.org/bot'

TEXT = 'Ура! Классный апдейт!'


MAX_COUNTER = 100
offset = -2
attempt = 0
chat_id: int
timeout = 60
# SEND_MESSAGE = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=AMAZING!'
link_list = (
    f'https://random.dog/woof.json',
    f'https://randomfox.ca/floof/'
)

# while counter < MAX_COUNTER:

while True:
    start_time = time.time()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&{timeout}').json()
    # updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={0}').json()
    random_image = requests.get(a:=random.choice(link_list)).json()
    print(f"[INFO] {attempt}", end=': ')
    pprint(updates)
    if updates:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            message = result['message']['text']
            if message == 'photo':
                text = random_image.get('image' if 'image' in a else 'url')
            else:
                text = f'Вы написали: {message}'
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
            print(result.get('message').get('from').get('first_name'), result.get('message').get('from').get('last_name'), message)


    # time.sleep(5)
    end_time = time.time()
    attempt += 1
    print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')