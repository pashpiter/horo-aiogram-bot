import random

from aiogram import F, Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config.bot import bot
from keyboards.horo import sign_kb
from texts.horo_text import ALL_HOROSCOPES
from texts.signs_info import SIGNS, SIGNS_LIST
from utils.horo import edit_kb_msg_answer_add_db, make_real_horo
from handlers.db_handlers import (horo_sign_from_db, insert_new_user,
                                  insert_or_update_kb_msg_id,
                                  insert_or_update_zodiak_msg_id,
                                  select_last_kb_msg_id,
                                  select_last_zodiak_msg_id,
                                  select_used_horo_for_user, update_zodiak)

router = Router()


@router.message(Command('help'))
async def command_help(message: Message) -> None:
    '''Команда help со списком доступных команд бота'''
    await message.answer(
        'Список доступных команд:\n'
        '/update для получения нового гороскопа\n'
        '/change_zodiac для изменения знака зодиака\n'
        '/clear_history для удаления истории сообщений'
        '/real_horoscope для получения реального гороскопа на сегодня'
    )


@router.message(F.text.lower().split()[0].in_(SIGNS_LIST))
async def sign_info_answer(message: Message) -> None:
    '''Фунция для отправки информации по знаку зодиака'''
    sign_in_db = await horo_sign_from_db(message.from_user.id)
    sign = sign_in_db[0].get('horo_sign')
    zodiak_msg = await message.answer(
            SIGNS[message.text.lower().split()[0]]
        )
    await insert_or_update_zodiak_msg_id(
        message.from_user.id, zodiak_msg.message_id
    )
    if not sign or sign != message.text.lower().split()[0]:
        await update_zodiak(
            message.from_user.id, message.text.lower().split()[0]
        )
    await send_horo(message)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    '''Команда start добаляет нового пользователя в базу или показывает
    доступные команды'''
    await insert_new_user(
        message.from_user.id,
        message.from_user.username
    )
    await message.answer(f'Привет, {html.bold(message.from_user.full_name)}!')
    zodiak_db = await horo_sign_from_db(message.from_user.id)
    zodiak: str = zodiak_db[0].get('horo_sign')
    if zodiak:
        await message.answer(
            f'Ты пользователь со знаком зодиака {zodiak.capitalize()}'
        )
        await message.answer(
            'Доступные команды:\n'
            '/update для получения нового гороскопа\n'
            '/change_zodiac для изменения знака зодиака\n'
            '/clear_history для удаления истории сообщений'
            '/real_horoscope для получения реального гороскопа на сегодня'
        )
    else:
        await change_zodiak(message)


@router.message(Command('update'))
async def update_horo(message: Message) -> None:
    '''Команда для получения (обновления) гороскопа'''
    await send_horo(message)


@router.message(Command('change_zodiac'))
async def change_zodiak(message: Message) -> None:
    '''Изменение или добавление знака зодиака'''
    await message.answer('Выбери свой знак зодиака 👇',
                         reply_markup=sign_kb())


@router.message(Command('clear_history'))
async def clear_history(message: Message) -> None:
    '''Удаление всех сообщений в чате за последние 48 часов'''
    ids_db = await select_last_zodiak_msg_id(
        message.from_user.id
    )
    last_zodiak_msg_id = ids_db[0].get('last_zodiak_msg_id')
    try:
        for msg_id in [
            n for n in range(
                message.message_id, 1, -1
            ) if n != last_zodiak_msg_id
        ]:
            await bot.delete_message(
                chat_id=message.chat.id, message_id=msg_id
            )
    except Exception as e:
        print(f'Ошибка удаления сообщения {e}')
    finally:
        await insert_or_update_kb_msg_id(
                message.from_user.id, None
            )


async def send_horo(message: Message) -> None:
    '''Подготовка и отправка гороскопа'''
    used_horo_db = await select_used_horo_for_user(message.chat.id)
    used_horo = [x['horo_id'] for x in used_horo_db] if used_horo_db else None
    kb_msg_id_db = await select_last_kb_msg_id(message.chat.id)
    kb_msg_id = kb_msg_id_db[0].get('last_kb_msg_id')
    if not used_horo:
        n = random.randint(1, len(ALL_HOROSCOPES))
        await edit_kb_msg_answer_add_db(message, kb_msg_id, n)
    elif len(used_horo) < len(ALL_HOROSCOPES):
        n = random.choice(
            [i for i in range(1, len(ALL_HOROSCOPES)+1) if i not in used_horo]
        )
        await edit_kb_msg_answer_add_db(message, kb_msg_id, n)
    else:
        await edit_kb_msg_answer_add_db(message, kb_msg_id)


@router.message(Command('real_horoscope'))
async def real_horo(message: Message) -> None:
    '''Команда для создания и отправки реального гороскопа'''
    zodiak_db = await horo_sign_from_db(message.from_user.id)
    horo = await make_real_horo(zodiak_db[0].get('horo_sign'))
    await message.answer(horo)


@router.message()
async def any_message(message: Message) -> None:
    '''Любое сообщение не подходящие под комманды или знаки зодиака'''
    await message.answer('Извините, я не понял')
