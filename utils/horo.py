from datetime import datetime

from aiogram import html
from aiogram.types import Message
from bs4 import BeautifulSoup
import httpx

from config.bot import bot
from handlers.db_handlers import (add_used_horo_to_user,
                                  insert_or_update_kb_msg_id)
from keyboards.horo import update_horo_kb
from texts.horo_text import ALL_HOROSCOPES
from texts.signs_info import SIGNS_IN_ENGLISH


async def get_cat_image() -> str:
    '''Получение адреса картинки фото с котиком'''
    url = 'https://api.thecatapi.com/v1/images/search'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()[0].get('url')


async def make_horo_msg(n: int) -> str:
    '''Подготовка текста гороскопа'''
    return (f'Гороскоп на {html.bold(datetime.now().strftime("%d.%m.%Y"))}:\n'
            f'{ALL_HOROSCOPES[n]}')
    # TODO добавить картинку


async def edit_kb_msg_answer_add_db(
    message: Message, kb_msg_id: int, n: int | None = None
) -> None:
    '''Удаление inline_kb у сообщения, отправка гороскопа, добаление номера
    гороскопа в БД'''
    msg = await make_horo_msg(n) if n else None
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=kb_msg_id
    ) if kb_msg_id else None

    answer_msg = await message.answer(
        msg, reply_markup=update_horo_kb()
    ) if msg else await message.answer_photo(
        photo=await get_cat_image(),
        caption=('Лимит гороскопов на сегодня исчерпан 😢\n'
                 'На сегодня есть только котики'),
        show_caption_above_media=True
    )

    await insert_or_update_kb_msg_id(
        message.chat.id,
        answer_msg.message_id if msg else None
    )
    await add_used_horo_to_user(message.chat.id, n) if n else None


async def get_real_horo(zodiak: str) -> str:
    '''Получение html реального гороскопа с сайта rambler'''
    url = f'https://horoscopes.rambler.ru/{zodiak}/'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text


async def make_real_horo(zodiak_ru: str) -> str:
    '''Делает реальный гороскоп по знаку зодиака'''
    zodiak = SIGNS_IN_ENGLISH[zodiak_ru]
    markup = await get_real_horo(zodiak)
    soup = BeautifulSoup(markup, "html.parser")
    a = soup.find('p', '_5yHoW AjIPq')
    return a.text
