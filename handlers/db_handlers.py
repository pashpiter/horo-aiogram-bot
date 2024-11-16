from datetime import date
from typing import Any

from asyncpg import Record

from config.db import create_connection


async def db_request(query: str, params: list = None) -> Any:
    '''Запрос к БД'''
    conn = await create_connection()
    try:
        if params:
            result = await conn.fetch(query, *params)
        else:
            result = await conn.fetch(query)
    except Exception as e:
        raise RuntimeError(f"Ошибка при запросе к базе данных: {e}")
    finally:
        await conn.close()
    return result


async def create_users_table() -> None:
    '''Создание базы данных users'''
    await db_request(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id INT UNIQUE NOT NULL,
            username VARCHAR(50),
            horo_sign VARCHAR(8)
        );
        '''
    )


async def create_horo_table():
    '''Созд'''
    await db_request(
        '''
        CREATE TABLE IF NOT EXISTS horoscopes (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
        '''
    )


async def create_user_horo_table() -> None:
    '''Создание базы данных для сохранения использваонных гороскопов'''
    await db_request(
        '''
        CREATE TABLE IF NOT EXISTS user_horo (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            horo_id INT NOT NULL,
            date DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        '''
    )
    # FOREIGN KEY(horo_id) REFERENCES horoscopes(id)


async def horo_sign_from_db(telegram_id: int) -> list[Record] | None:
    '''Возращает знак зодиака для user'''
    result = await db_request(
        '''
        SELECT horo_sign FROM users WHERE telegram_id=$1
        ''', [telegram_id,]
    )
    return result


async def insert_new_user(telegram_id: int, username: str) -> None:
    '''Добавляет нового пользовтеля в users'''
    await db_request(
        '''
        INSERT INTO users (telegram_id, username)
        VALUES ($1, $2) ON CONFLICT DO NOTHING
        ''', [
            telegram_id,
            username
        ]
    )


async def select_used_horo_for_user(telegram_id: int) -> list[Record] | None:
    date_today = date.today()
    result = await db_request(
        '''
        SELECT user_horo.horo_id FROM user_horo
        JOIN users ON users.id = user_horo.user_id
        WHERE user_horo.date::date = $1 AND users.telegram_id = $2
        ''', [
            date_today,
            telegram_id
        ]
    )
    return result


async def add_used_horo_to_user(telegram_id: int, horo_id: int) -> None:
    '''Добаление id использованного гороскопа в бд'''
    await db_request(
        '''
        INSERT INTO user_horo (user_id, horo_id)
        VALUES ((SELECT id from users WHERE telegram_id = $1), $2)
        ''', [
            telegram_id,
            horo_id
        ]
    )


async def update_zodiak(telegram_id: int, horo_sign: str) -> None:
    '''Обновление знака зодиака пользователя'''
    await db_request(
        '''
        UPDATE users
        SET horo_sign = $1 WHERE telegram_id = $2
        ''', [
            horo_sign,
            telegram_id
        ]
    )


async def create_first_last_msg_ids_table() -> None:
    '''Создание таблицы для хранения id первого сообщения в чате,
    id последнего сообщения с inline_keyboard, id последнего сообщения со
    знаком зодиака'''
    await db_request(
        '''
        CREATE TABLE IF NOT EXISTS msg_ids (
            id SERIAL PRIMARY KEY,
            user_id INT UNIQUE NOT NULL,
            last_kb_msg_id INT,
            last_zodiak_msg_id INT,
            first_in_chat_msg_id INT DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        '''
    )


async def insert_or_update_kb_msg_id(
        telegram_id: int, message_id: int
) -> None:
    '''Добавить или обновить id последнего сообщения с inline_keyboard'''
    result = await db_request(
        '''
        SELECT msg_ids.* FROM msg_ids
        JOIN users ON users.id = msg_ids.user_id
        WHERE users.telegram_id = $1
        ''', [
            telegram_id
        ]
    )
    if result:
        await db_request(
            '''
            UPDATE msg_ids SET last_kb_msg_id = $1
            WHERE user_id = $2
            ''', [
                message_id,
                result[0].get('user_id')
            ]
        )
    else:
        await db_request(
            '''
            INSERT INTO msg_ids (user_id, last_kb_msg_id)
            VALUES ($1, $2)
            ''', [
                result[0].get('user_id'),
                message_id
            ]
        )


async def insert_or_update_zodiak_msg_id(
        telegram_id: int, message_id: int
) -> None:
    '''Добавить или обновить id последнего сообщения со знаком зодиака'''
    result = await db_request(
        '''
        SELECT msg_ids.* FROM msg_ids
        JOIN users ON users.id = msg_ids.user_id
        WHERE users.telegram_id = $1
        ''', [
            telegram_id
        ]
    )
    if result:
        await db_request(
            '''
            UPDATE msg_ids SET last_zodiak_msg_id = $1
            WHERE user_id = $2
            ''', [
                message_id,
                result[0].get('user_id')
            ]
        )
    else:
        await db_request(
            '''
            INSERT INTO msg_ids (user_id, last_zodiak_msg_id)
            VALUES ($1, $2)
            ''', [
                result[0].get('user_id'),
                message_id
            ]
        )


async def select_last_zodiak_msg_id(telegram_id: int) -> list[Record]:
    '''Получить id первого сообщения в чате и последнего
    сообщения со знаком зодиака'''
    result = await db_request(
        '''
        SELECT msg_ids.last_zodiak_msg_id
        FROM msg_ids
        JOIN users ON users.id = msg_ids.user_id
        WHERE users.telegram_id = $1
        ''', [
            telegram_id
        ]
    )
    return result


async def select_last_kb_msg_id(telegram_id: int) -> list[Record] | None:
    '''Получить id последнего сообщения с inline_keyboard'''
    result = await db_request(
        '''
        SELECT msg_ids.last_kb_msg_id FROM msg_ids
        JOIN users ON users.id = msg_ids.user_id
        WHERE users.telegram_id = $1
        ''', [
            telegram_id
        ]
    )
    return result


async def create_tables() -> None:
    '''Создание всех таблиц'''
    await create_users_table()
    await create_user_horo_table()
    await create_user_horo_table()
    await create_first_last_msg_ids_table()


async def select_users_without_horo_today() -> list[Record] | None:
    result = await db_request(
        '''
        WITH u AS (
            SELECT DISTINCT user_id FROM user_horo
            WHERE date = CURRENT_DATE
        )
        SELECT telegram_id FROM users
        WHERE id NOT IN (SELECT * FROM u)
        '''
    )
    return result
