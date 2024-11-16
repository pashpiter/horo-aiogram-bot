from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.commands import send_horo

router = Router()


@router.callback_query(F.data == 'update')
async def update_callback(call: CallbackQuery):
    '''Обработака inline_kb Обновить'''
    await send_horo(call.message)
