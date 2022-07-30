from django.db.models import Count
from telebot.handler_backends import StatesGroup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bots.models import User, TempBask


class UserState(StatesGroup):
    start = 0
    sub_category = 1
    sub_category_detail = 2
    back = 3
    back_category = 4
    user_name = 5


def gen_markup(message=None):
    try:
        product_qty = TempBask.objects.filter(chat_id=message.from_user.id).values('qty').annotate(
            count=Count('qty')).get()
        if product_qty:
            print('sasasasasaslllllola')
            # print(message.message.json['reply_markup']['inline_keyboard'][0][1]['text'], 'uy')
            markup = InlineKeyboardMarkup()
            markup.row_width = 3
            qty_count = product_qty['count'] + 1
            print(qty_count, ' gen_markup()')
            markup.add(InlineKeyboardButton("-", callback_data="subtract"),
                       InlineKeyboardButton(f"{'<>'}", callback_data="qty_1"),
                       InlineKeyboardButton("+", callback_data="add"),
                       InlineKeyboardButton("📥 Savatga qo\'shish", callback_data="📥 Savatga qo\'shish"))
            print('dsaddadsadasdasdsa')
            return markup
    except:
        # product_qty = TempBask.objects.filter(chat_id=message.from_user.id).values('qty').annotate(
        #     count=Count('qty')).get()
        # print(product_qty, 'gen_metcub')
        # if product_qty['count']:
        #     qty_count = product_qty['count'] + 1
        # else:
        #     qty_count = 1

        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        markup.add(InlineKeyboardButton("-", callback_data="subtract"),
                   InlineKeyboardButton(f"{'<>'}", callback_data="qty_1"),
                   InlineKeyboardButton("+", callback_data="add"),
                   InlineKeyboardButton("📥 Savatga qo\'shish", callback_data="📥 Savatga qo\'shish"))
        return markup


def basket_product(message):
    pass
