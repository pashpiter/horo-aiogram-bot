import asyncio
import logging
import sys
from os import getenv

from aiogram import Dispatcher
from dotenv import load_dotenv

from config.bot import setup_bot
from config.scheduler import setup_scheduler
from handlers.callbacks import router as callback_router
from handlers.commands import router as commands_router
from handlers.db_handlers import create_tables

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


async def main() -> None:
    '''Основная логика программы'''
    await create_tables()
    dp.include_router(commands_router)
    dp.include_router(callback_router)
    bot = await setup_bot()
    scheduler = await setup_scheduler()
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
