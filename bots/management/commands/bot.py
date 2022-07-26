import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot import TeleBot
from telebot import custom_filters

from bots.user_state import UserState, gen_markup
from django.core.management.base import BaseCommand
from bots.views import models_method
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


@bot.message_handler(commands=['del'])
def delete(message):
    rmv = ReplyKeyboardRemove()
    user = User.objects.get(chat_id=message.from_user.id).delete()
    bot.send_message(message.from_user.id, 'ochirildi', reply_markup=rmv)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.set_state(message.from_user.id, UserState.user_name, message.chat.id)
    bot.send_message(message.chat.id, 'Assalomu Alekum Ism kirgiz')


@bot.message_handler(state=UserState.user_name)
def user_name(message):
    user_id = message.from_user.id
    try:
        user = User.objects.filter(chat_id=user_id).exists()
        if not user:
            User.objects.create(chat_id=user_id, username=message.text)
        else:
            print('user alredy exists')
        # if not user:
        #     user.save()
        markup = ReplyKeyboardMarkup(True, row_width=2)
        btn_category = ProductCategory.objects.values('category_name')
        res = []
        for btn in btn_category:
            a = btn['category_name']
            res.append(a)
        rkm = markup.add(*res, '⬅savt')
        bot.set_state(user_id, UserState.sub_category, message.chat.id)
        bot.send_message(message.chat.id, 'Bolimni tanlang 1', reply_markup=rkm)
    except:
        print('hatolik')
        bot.send_message(message.chat.id, 'Bolimni tanlang +1', reply_markup=rkm)


@bot.message_handler(state=UserState.sub_category)
def sub_category(message):
    if message.text == '⬅️ orqga':
        # bot.set_state(message.from_user.id, UserState.user_name)
        return user_name(message)
    markup = ReplyKeyboardMarkup(True, row_width=2)
    models = ProductSubCategory.objects.all()

    print(models, "++++!11")

    res = []
    if models:
        for btn in models:
            print(btn)
    #         a = btn['sub_categoty_name']
    #         res.append(a)
    #
    # rkm = markup.add(*res, '⬅️ orqga')
    # bot.set_state(message.from_user.id, UserState.sub_category_detail, message.chat.id)
    # bot.send_message(message.from_user.id, 'Bolimni tanlang 2 ', reply_markup=rkm)


@bot.message_handler(state=UserState.sub_category_detail)
def sub_category_detail(message):
    try:
        if message.text == '⬅️ orqga':
            # bot.set_state(message.from_user.id, UserState.user_name)
            return sub_category(message)
        markup = ReplyKeyboardMarkup(True, row_width=2)
        models = ProductSubCategoryDetail.objects.filter(sub_categoty_name=message.text).values('sub_categoty_name',
                                                                                                'sub_category_image',
                                                                                                'product_price',
                                                                                                'deskripsiyon')
        print(models)
        res = []
        for i in models:
            res.append(i)
        data = f"Nomi: {res[0]['sub_categoty_name']} \n{res[0]['deskripsiyon']}" \
               f"\nNarxi: {res[0]['product_price']}"
        sa = res[0]['sub_category_image']
        photo = open(sa, 'rb')
        bot.send_photo(message.from_user.id, photo, data, reply_markup=gen_markup())
        photo.close()
    except:
        print('hatolik detal')
    # finally:
    #     photo.close()


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.enable_saving_states()

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     print('adsada')
#     btn_category = ProductCategory.objects.all()
#     print(btn_category)
#     bot.send_message(message.chat.id, 'olasas')
