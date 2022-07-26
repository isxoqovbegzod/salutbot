from telebot.handler_backends import State, StatesGroup  # States
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class UserState(StatesGroup):
    start = 0
    sub_category = 1
    sub_category_detail = 2
    back = 3
    back_category = 4
    user_name = 5


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("+", callback_data="add"),
               InlineKeyboardButton("1", callback_data="qty_1"),
               InlineKeyboardButton("-", callback_data="subtract"))
    return markup
