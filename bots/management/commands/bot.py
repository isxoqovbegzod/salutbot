import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot import TeleBot
from telebot import custom_filters

from bots.user_state import UserState, gen_markup, basket_product
from django.core.management.base import BaseCommand
from bots.views import models_method
from bots.models import ProductCategory, ProductSubCategory, ProductSubCategoryDetail, User, TempBask, Basket
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
        if message.text == '📥 Savat':
            basket_product(message)
            bot.send_message(message.from_user.id, 'olma 📥 Savat')
        user = User.objects.filter(chat_id=user_id).exists()
        if not user:
            User.objects.create(chat_id=user_id, username=message.text)
        else:
            print('user alredy exists')
        # if not user:
        #     user.save()
        markup = ReplyKeyboardMarkup(True, row_width=2)
        btn_category = ProductCategory.objects.values('category_name')
        if btn_category:
            res = []
            for btn in btn_category:
                a = btn['category_name']
                res.append(a)
        rkm = markup.add(*res, '📥 Savat')
        bot.set_state(user_id, UserState.sub_category, message.chat.id)
        bot.send_message(message.chat.id, 'Bolimni tanlang 1', reply_markup=rkm)
    except:
        print('hatolik')
        bot.send_message(message.chat.id, 'Bolimni tanlang +1', reply_markup=rkm)


@bot.message_handler(state=UserState.sub_category)
def sub_category(message):
    print(message.text, 'test')
    try:
        if message.text == '⬅️ orqga':
            return user_name(message)

        markup = ReplyKeyboardMarkup(True, row_width=2)

        models = ProductSubCategory.objects.filter(product_categoty__category_name=message.text).values(
            'product_sub_cat', 'category_image')

        print(models, "++++!11")

        result = []
        image = []
        print(result)
        res = []
        if models:
            for btn in models:
                if not image:
                    image.append(btn['category_image'])
                olma = ProductSubCategoryDetail.objects.filter(id=btn['product_sub_cat']).values(
                    'sub_categoty_name').get()
                print(olma, 'olma')
                result.append(olma['sub_categoty_name'])
            print(result)
            print(image)
            photo = open(*image, 'rb')
        else:
            return user_name(message)

        rkm = markup.add(*result, '⬅️ orqga', '📥 Savat')

        bot.set_state(message.from_user.id, UserState.sub_category_detail, message.chat.id)
        bot.send_photo(message.from_user.id, photo, reply_markup=rkm)
        photo.close()
    except:
        print('hatolik sub_category()')
        # photo.close()
    # finally:
    #     photo.close()


@bot.message_handler(state=UserState.sub_category_detail)
def sub_category_detail(message):
    try:
        if message.text == '⬅️ orqga':
            message.text = 'hello'
            return sub_category(message)
        if message.text == '📥 Savat':
            print('sub_category_detail()  -> savat')
            bot.send_message(message.chat.id, 'savat detail')

        markup = ReplyKeyboardMarkup(True, row_width=2)
        models = ProductSubCategoryDetail.objects.filter(sub_categoty_name=message.text).values('sub_categoty_name',
                                                                                                'sub_category_image',
                                                                                                'product_price',
                                                                                                'deskripsiyon')
        print(models)
        if models:
            res = []
            for i in models:
                res.append(i)
            data = f"Nomi: {res[0]['sub_categoty_name']} \n{res[0]['deskripsiyon']}" \
                   f"\nNarxi: {res[0]['product_price']}"
            sa = res[0]['sub_category_image']
            photo = open(sa, 'rb')
        else:
            return sub_category(message)
        print('))))))))))))))))))))))))))))))')
        bot.send_photo(message.from_user.id, photo, data, reply_markup=gen_markup(message))
        print('))))))))))))))))))))))))))))))22')

        photo.close()
    except:
        print('hatolik detal')
    # finally:
    #     photo.close()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'add':
        a = call.message.caption
        ds = ''
        for i in a:
            ds += '1'
            if i == '\n':
                break
        res = len(ds) - 2
        olma = a[6:res]
        user = ProductSubCategoryDetail.objects.filter(sub_categoty_name=olma).values('sub_categoty_name',
                                                                                      'product_qty',
                                                                                      'product_price').get()
        print(user)
        user_tempbask = TempBask(chat_id=call.from_user.id, product_name=user['sub_categoty_name'],
                                 product_price=user['product_price'], qty=user['product_qty'])

        user_tempbask.save()
        bot.answer_callback_query(call.id, f"{1} ta")
    elif call.data == '📥 Savatga qo\'shish':
        basket(call)
        bot.answer_callback_query(call.id, "Qo'shildi ")




@bot.message_handler(commands=['📥 Savatga qo\'shish'])
def basket(message):
    user_product_data = TempBask.objects.filter(chat_id=message.from_user.id).values('product_name',
                                                                                     'product_price', 'qty')

    # res = int(user_product_data['product_price']) * len(user_product_data['qty'])
    # print(res)
    res = []
    for i in user_product_data:
        res.append(i)

    len_qty = len(res) - 1
    price_product_sum = float(res[0]['product_price']) * len_qty
    user_basc = Basket(chat_id=message.from_user.id, product_name=res[0]['product_name'],
                       product_price=price_product_sum, qty=len_qty)
    user_basc.save()

    #     txt += f'🔹<b>{i["product"]}</b>\n' \
    #            f'{i["count"]} x {i["price"]} = {int(i["price"]) * int(i["count"]):,} \n\n'
    #     x += i["price"] * int(i["count"])
    #     txt_rus += f'🔹<b>{i["product"]}</b>\n' \
    #                f'{i["count"]} x {i["price"]} = {int(i["price"]) * int(i["count"]):,} \n\n'
    # txt += f'<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')
    # txt_rus += f'<b>Общий:</b> {x:,} sum'.replace(',', ' ')

    # print(call.message.json['message_id'])
    # pass
    # a = call.message.caption
    # ds = ''
    # for i in a:
    #     ds += '1'
    #     if i == '\n':
    #         break
    # res = len(ds) - 1
    # olma = a[6:res]
    # print(olma)

    # user = User.objects.filter(chat_id=call.from_user.id).values('id', 'qty').get()
    # user['qty'] = {'data': 1}
    #
    # print(user)
    # sa = User(id=user['id'], chat_id=call.from_user.id, qty=user['qty'])
    # sa.save()
    # gen_markup(call)


@bot.message_handler(commands=['📥 Savatga'])
def basket_detail(message):
    pass


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.enable_saving_states()

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     print('adsada')
#     btn_category = ProductCategory.objects.all()
#     print(btn_category)
#     bot.send_message(message.chat.id, 'olasas')
