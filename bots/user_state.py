from django.db.models import Count
from telebot.handler_backends import StatesGroup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
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
                       InlineKeyboardButton("👈👉", callback_data="qty_1"),
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
                   InlineKeyboardButton("👈👉", callback_data="qty_1"),
                   InlineKeyboardButton("+", callback_data="add"),
                   InlineKeyboardButton("📥 Savatga qo\'shish", callback_data="📥 Savatga qo\'shish"))
        return markup


def get_order_product(message):
    try:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("⬅️orqga", callback_data="⬅️orqga"),
                   InlineKeyboardButton("🚖 Buyurtma berish", callback_data="order"),
                   InlineKeyboardButton("🗑 Savatni tozalash", callback_data="basket_remove"))
        print('get_order_product all()')
        return markup
    except:
        print('hatolik get_order_product ')


def confirm(message):
    """confirm - tasdiqlash """
    try:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('❌', callback_data='no'),
                   InlineKeyboardButton('✅', callback_data='ok'),
                   InlineKeyboardButton('Buyurtmani tasdiqlang', callback_data='Buyurtmani tasdiqlang'))

        return markup
    except:
        print('hatolik confirm')















