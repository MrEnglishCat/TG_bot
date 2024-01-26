import asyncio
import logging

from rock_paper_scissors_bot.bot_data.config_data.config import load_config
from aiogram import Bot, Dispatcher
from rock_paper_scissors_bot.bot_data.handlers import user_handlers, other_handlers

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')


    bot = Bot(token=load_config('.env').tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()
    logger.info('Starting bot')


    dp.include_routers(
        user_handlers.router,
        other_handlers.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
