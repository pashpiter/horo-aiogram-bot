from os import getenv

import asyncpg


async def create_connection() -> asyncpg.Connection:
    '''Создание подключения к БД'''
    user = getenv('DB_USER')
    password = getenv('DB_PASSWORD')
    db_name = getenv('DB_NAME')
    host = getenv('DB_HOST')
    port = getenv('DB_PORT')
    url = f'postgres://{user}:{password}@{host}:{port}/{db_name}'
    return await asyncpg.connect(url)
