from config_data.config import load_config
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from handlers import user_handlers, other_handlers


bot = Bot(token=load_config('.env').tg_bot.token)
dp = Dispatcher()

user = {
    'bot_item': None,
    'user_item': None,
    'win': None,
    'total_games': 0
}

# dp.include_router(user_handlers.router)
# dp.include_router(other_handlers.router)

dp.include_routers(
    user_handlers.router,
    other_handlers.router
)

if __name__ == '__main__':
    dp.run_polling(bot)

