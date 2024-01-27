import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from environs import Env


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/command_1': 'command_1 desription',
    '/command_2': 'command_2 desription',
    '/command_3': 'command_3 desription',
    '/command_4': 'command_4 desription'
}

# Создаем асинхронную функцию
# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS_RU.items()
    ]
    await bot.set_my_commands(main_menu_commands)

async def main():
    env = Env()
    env.read_env()
    BOT_TOKEN = env('BOT_TOKEN')
    # Создаем объекты бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    await set_main_menu(bot)
    # await dp.startup.register(bot)
    # await dp.run_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())