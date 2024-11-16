from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup


def sign_kb() -> ReplyKeyboardMarkup:
    '''Возвращает Replay kb со знаками зодиака'''
    buttons = [
        [KeyboardButton(text='Овен ♈'), KeyboardButton(text='Телец ♉'),
         KeyboardButton(text='Близнецы ♊'), KeyboardButton(text='Рак ♋')],

        [KeyboardButton(text='Лев ♌'), KeyboardButton(text='Дева ♍'),
         KeyboardButton(text='Весы ♎'), KeyboardButton(text='Скорпион ♏')],

        [KeyboardButton(text='Стрелец ♐'), KeyboardButton(text='Козерог ♑'),
         KeyboardButton(text='Водолей ♒'), KeyboardButton(text='Рыбы ♓')]
    ]
    replay_keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        one_time_keyboard=True,
        input_field_placeholder='Выберите знак зодиака на клавиатуре'
    )
    return replay_keyboard


def update_horo_kb() -> InlineKeyboardMarkup:
    '''Возвращает Inline kb с кнопкой Обновить'''
    button = InlineKeyboardButton(text='Обновить', callback_data='update')
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return inline_keyboard
