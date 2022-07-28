from telebot.handler_backends import State, StatesGroup  # States
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bots.models import User

class UserState(StatesGroup):
    start = 0
    sub_category = 1
    sub_category_detail = 2
    back = 3
    back_category = 4
    user_name = 5

def gen_markup(message=None):
    print('message')
    try:
        if message.message.json['reply_markup']['inline_keyboard'][0][1]['text']:
            print('sasasasasaslllllola')
            print(message.message.json['reply_markup']['inline_keyboard'][0][1]['text'], 'uy')
            user = User.objects.filter(chat_id=message.from_user.id).values('qty').get()
            markup = InlineKeyboardMarkup()
            markup.row_width = 3
            p = user['qty']
            res = message.message.json['reply_markup']['inline_keyboard'][0][1]['text'] = p
            markup.add(InlineKeyboardButton("-", callback_data="subtract"),
                    InlineKeyboardButton(f"{res}", callback_data="qty_1"),
                    InlineKeyboardButton("+", callback_data="add"))
            print('dsaddadsadasdasdsa')
    except:
        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        markup.add(InlineKeyboardButton("-", callback_data="subtract"),
                InlineKeyboardButton("1", callback_data="qty_1"),
                InlineKeyboardButton("+", callback_data="add"))
        print('dsaddadsadasdasdsa22')
    return markup

def basket_product(message):
    pass