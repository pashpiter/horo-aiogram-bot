from config.bot import bot
from handlers.commands import send_horo
from handlers.db_handlers import select_users_without_horo_today


async def daily_horo() -> None:
    '''Задача для планировщика отправляющее гороскоп всем пользователям
    не получавших его сегодня'''
    users_db = await select_users_without_horo_today()
    users_ids = [user['telegram_id'] for user in users_db]
    for user_id in users_ids:
        msg = await bot.send_message(
            chat_id=user_id, text=(
                'Ежедневный гороскоп для тех кто его сегодня не получал'
            )
        )
        await send_horo(msg)
