import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot import TeleBot
from telebot import custom_filters

from django.core.management.base import BaseCommand
from bots.views import models_method
from telebot.handler_backends import State, StatesGroup  # States
from bots.models import ProductCategory, ProductSubCategory, ProductSubCategoryDetail, User
from bots.views import choice_sub_categoty

# Объявление переменной бота
bot = TeleBot(token='5369814485:AAFXt0RAqq7ixRgMxW5CIW3hKNlWiM9ZNWo', threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        # bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        # bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.infinity_polling()


class UserState(StatesGroup):
    start = 0
    sub_category = 1
    sub_category_detail = 2
    back = 3
    back_category = 4


@bot.message_handler(commands=['del'])
def delete(message):
    rmv = ReplyKeyboardRemove()

    bot.send_message(message.from_user.id, 'ochirildi', reply_markup=rmv)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = User.objects.filter(chat_id=message.from_user.id)
    markup = ReplyKeyboardMarkup(True)
    btn_category = ProductCategory.objects.values('category_name')
    res = []
    for btn in btn_category:
        a = btn['category_name']
        res.append(a)
    rkm = markup.add(*res)
    bot.set_state(message.from_user.id, UserState.sub_category, message.chat.id)
    bot.send_message(message.chat.id, 'Привет!', reply_markup=rkm)


@bot.message_handler(state=UserState.sub_category)
def sub_category(message):
    if message.text == '⬅️ orqga':
        bot.set_state(message.from_user.id, UserState.back_category)
        print(message.text)
    markup = ReplyKeyboardMarkup(True)
    models = ProductSubCategoryDetail.objects.filter(connect_product_categoty__category_name=message.text).values(
        'sub_categoty_name')
    res = []
    if models:
        for btn in models:
            a = btn['sub_categoty_name']
            res.append(a)

    rkm = markup.add(*res)
    rkm = markup.row('⬅️ orqga')

    bot.send_message(message.from_user.id, 'Bolimni tanlang', reply_markup=rkm)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.enable_saving_states()

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     print('adsada')
#     btn_category = ProductCategory.objects.all()
#     print(btn_category)
#     bot.send_message(message.chat.id, 'olasas')
