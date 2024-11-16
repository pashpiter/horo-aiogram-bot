from os import getenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def setup_bot() -> Bot:
    '''Настройка бота'''
    commands = [
        BotCommand(
            command='start',
            description='Стартовая команда'
        ),
        BotCommand(
            command='help',
            description='Список доступных команд'
        ),
        BotCommand(
            command='update',
            description='Обновление гороскопа'
        ),
        BotCommand(
            command='change_zodiac',
            description='Изменение знака зодиака'
        ),
        BotCommand(
            command='real_horoscope',
            description='Реальный гороскоп'
        ),
        BotCommand(
            command='clear_history',
            description='Удаление всех сообщений в чате за поледние 48 часов'
        ),
    ]
    await bot.set_my_commands(commands)
    return bot
