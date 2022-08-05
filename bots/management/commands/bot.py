from django.db.models import Count
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot import TeleBot
from telebot import custom_filters

from bots.user_state import UserState, gen_markup, get_order_product, confirm
from django.core.management.base import BaseCommand
from bots.models import ProductCategory, ProductSubCategory, ProductSubCategoryDetail, User, TempBask, Basket, Settings
from bots.views import choice_sub_categoty
from geopy.geocoders import Nominatim

# Объявление переменной бота
bot = TeleBot(token='5536054627:AAGQan5uziLaZME577B3tX5ayeks7Q1fCLY', threaded=False)



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
            print("sasassssssssssssssssssss----------------->>>>>>>>>>>>>>>> 1")
            return basket_detail(message)
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
        if message.text == '⬅️orqga':
            return user_name(message)
        elif message.text == '📥 Savat':
            return basket_detail(message)
        markup = ReplyKeyboardMarkup(True, row_width=2)

        models = ProductSubCategory.objects.filter(product_categoty__category_name=message.text).values(
            'product_sub_cat', 'category_image')

        result = []
        image = []
        res = []
        if models:
            for btn in models:
                if not image:
                    image.append(btn['category_image'])
                olma = ProductSubCategoryDetail.objects.filter(id=btn['product_sub_cat']).values(
                    'sub_categoty_name').get()
                result.append(olma['sub_categoty_name'])
            photo = open(*image, 'rb')
        else:
            return user_name(message)

        rkm = markup.add(*result, '⬅️ orqga', '📥 Savat')

        bot.set_state(message.from_user.id, UserState.sub_category_detail, message.chat.id)
        bot.send_photo(message.from_user.id, photo, reply_markup=rkm)
        photo.close()
    except:
        print('hatolik sub_category()')


@bot.message_handler(state=UserState.sub_category_detail)
def sub_category_detail(message):
    try:
        if message.text == '⬅️ orqga':
            return sub_category(message)
        if message.text == '📥 Savat':
            return basket_detail(message)

        markup = ReplyKeyboardMarkup(True, row_width=2)
        models = ProductSubCategoryDetail.objects.filter(sub_categoty_name=message.text).values('sub_categoty_name',
                                                                                                'sub_category_image',
                                                                                                'product_price',
                                                                                                'deskripsiyon')
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
        bot.send_photo(message.from_user.id, photo, data, reply_markup=gen_markup(message))
        photo.close()
    except:
        print('hatolik detal')


@bot.message_handler(content_types=['location'])
def handle_location(message):
    try:
        locations = {'lat': message.location.latitude, 'long': message.location.longitude}
        user = User.objects.get(chat_id=message.from_user.id)
        user.locations = locations
        user.save()
        user_phone(message)
    except:
        print('locations hatolik')


@bot.message_handler(content_types=['contact'])
def handler_phone(message):
    try:
        print(message.contact.phone_number, '++++++++')
        phone = message.contact.phone_number
        user = User.objects.get(chat_id=message.from_user.id)
        user.phone_number = phone
        user.save()
        rkm = ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Buyurtmani Tasdiqlang", reply_markup=rkm)
        product_approval(message)
    except:
        print('phone number hatolik')


def product_approval(message):
    try:
        filer_count_product = Basket.objects.filter(chat_id=message.from_user.id).values('product_name', 'qty',
                                                                                         'product_price')
        toll_price = Settings.objects.values('toll_price').get()
        base = []
        price = 0
        for res in filer_count_product:
            base.append(res)
            price += float(res['product_price'])

        sum_price = price + toll_price['toll_price']
        user_location = User.objects.filter(chat_id=message.from_user.id).values('locations').get()
        geolocator = Nominatim(user_agent="bots")
        location = geolocator.reverse(f"{user_location['locations']['lat']}, {user_location['locations']['long']}")
        if filer_count_product:
            text = f'Sizning Buyurtmangiz: \nManzil: {location}\n\n'
            for i in base:
                text += f"\n{i['qty']} ✖ {i['product_name']}"

            text += f'\n\nYetkazib berish: {toll_price["toll_price"]} \nJami: {sum_price} '
            bot.send_message(message.from_user.id, text, reply_markup=confirm(message))
        else:
            bot.send_message(message.from_user.id, "savatda hech nima yo'q")
    except:
        print('hatolik product_approval')


def user_locations(message):
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = KeyboardButton(text="📍 Geolocatsiyani yuboring", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.from_user.id, '📍 Geolocatsiyani yuborish', reply_markup=keyboard)


def user_phone(message):
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text='📞 Telefon raqam yuboring', request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.from_user.id, '📞 Telefon raqam yuboring', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == 'add':
            a = call.message.caption
            ds = ''
            for i in a:
                ds += '1'
                if i == '\n':
                    break
            res = len(ds) - 2
            product_name = a[6:res]
            user = ProductSubCategoryDetail.objects.filter(sub_categoty_name=product_name).values('sub_categoty_name',
                                                                                                  'product_qty',
                                                                                                  'product_price').get()
            user_tempbask = TempBask(chat_id=call.from_user.id, product_name=user['sub_categoty_name'],
                                     product_price=user['product_price'], qty=user['product_qty'])
            user_tempbask.save()
            product_qty = TempBask.objects.filter(chat_id=call.from_user.id).values('qty').annotate(
                count=Count('qty')).get()
            qty_count = product_qty['count']
            bot.answer_callback_query(call.id, f"{qty_count} ta")
        elif call.data == '📥 Savatga qo\'shish':
            basket(call)
            bot.answer_callback_query(call.id, "Qo'shildi !")
            TempBask.objects.filter(chat_id=call.from_user.id).delete()
            bot.delete_message(call.from_user.id, call.message.message_id)
        elif call.data == 'subtract':
            a = call.message.caption
            ds = ''
            for i in a:
                ds += '1'
                if i == '\n':
                    break
            res = len(ds) - 2
            product_name = a[6:res]

            # product_qty = TempBask.objects.filter(chat_id=call.from_user.id).values('qty').annotate(
            #     count=Count('qty')).get()

            if product_qty := TempBask.objects.filter(chat_id=call.from_user.id).values('qty').annotate(
                    count=Count('qty')).get():
                model_tempbask = TempBask.objects.filter(chat_id=call.from_user.id).filter(
                    product_name=product_name).first().delete()
                qty_count = product_qty['count'] - 1

                bot.answer_callback_query(call.id, f"{qty_count} ta")
            else:
                bot.answer_callback_query(call.id, "0 ta")
        elif call.data == 'order':
            bot.delete_message(call.from_user.id, call.message.message_id)
            user_locations(call)
        elif call.data == 'basket_remove':
            user_product = Basket.objects.filter(chat_id=call.from_user.id).all()
            user_product.delete()
            bot.delete_message(call.from_user.id, call.message.message_id)
            sub_category(call.message)
        elif call.data == '⬅️orqga':
            rkm = ReplyKeyboardRemove()
            sub_category(call.message)
            bot.delete_message(call.from_user.id, call.message.message_id)

        elif call.data == 'no':
            user_product = Basket.objects.filter(chat_id=call.from_user.id).all()
            user_product.delete()
            sub_category(call.message)
        elif call.data == 'ok':
            try:
                filer_count_product = Basket.objects.filter(chat_id=call.from_user.id).values('product_name', 'qty',
                                                                                              'product_price')
                toll_price = Settings.objects.values('toll_price').get()
                base = []
                price = 0
                for res in filer_count_product:
                    base.append(res)
                    price += float(res['product_price'])
                sum_price = price + toll_price['toll_price']
                user_data = User.objects.filter(chat_id=call.from_user.id).values('locations', 'username',
                                                                                  'phone_number').get()
                geolocator = Nominatim(user_agent="bots")
                location = geolocator.reverse(f"{user_data['locations']['lat']}, {user_data['locations']['long']}")
                if filer_count_product:
                    text = f'Yangi Buyurtma: \nManzil: {location}\n\nIsm: {user_data["username"]}\nTelefon: {user_data["phone_number"]}'
                    for i in base:
                        text += f"\n{i['qty']} ✖ {i['product_name']}"

                    text += f'\n\nYetkazib berish: {toll_price["toll_price"]} \nJami: {sum_price} '
                    bot.send_message(-1001787326459, text)
                    user_product = Basket.objects.filter(chat_id=call.from_user.id).all()
                    user_product.delete()

                    sub_category(call.message)
            except:
                print('ok  hatolik')

    except:
        bot.answer_callback_query(call.id, "0 ta")
        print('call   hatolik')


def gen_markup_remove(message):
    rkm_remove = ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Bo\'limni tanlang', reply_markup=rkm_remove)


@bot.message_handler(commands=['📥 Savatga qo\'shish'])
def basket(message):
    try:
        user_product_data = TempBask.objects.filter(chat_id=message.from_user.id).values('product_name',
                                                                                         'product_price').annotate(
            count=Count('product_name'))

        res = []
        for i in user_product_data:
            res.append(i)

        osss = []
        if res_product := Basket.objects.filter(chat_id=message.from_user.id).filter(
                product_name=res[0]['product_name']).all():
            osss = res_product.values('qty').get()
            res_product.delete()
            result = osss['qty'] + res[0]['count']
            reult_price = result * float(res[0]['product_price'])
            user_product = Basket(chat_id=message.from_user.id, qty=result,
                                  product_price=reult_price, product_name=res[0]['product_name'])
            user_product.save()
        else:
            result_price = res[0]['count'] * float(res[0]['product_price'])
            user_product = Basket(chat_id=message.from_user.id, qty=res[0]['count'],
                                  product_price=result_price, product_name=res[0]['product_name'])
            user_product.save()

    except:
        bot.answer_callback_query(message.from_user.id, "Qo'shilmagan")
        print('📥 Savatga qo\'shish hatolik')


@bot.message_handler(commands=['📥 Savat'])
def basket_detail(message):
    try:
        filer_count_product = Basket.objects.filter(chat_id=message.from_user.id).values('product_name', 'qty',
                                                                                         'product_price')
        print(filer_count_product)
        toll_price = Settings.objects.values('toll_price').get()
        base = []
        price = 0
        for res in filer_count_product:
            base.append(res)
            price += float(res['product_price'])

        sum_price = price + toll_price['toll_price']

        if filer_count_product:
            text = 'Savatda: '
            for i in base:
                text += f"\n{i['qty']} ✖ {i['product_name']}"

            text += f'\nYetkazib berish: {toll_price["toll_price"]} \nJami: {sum_price} '
            bot.send_message(message.from_user.id, text, reply_markup=get_order_product(message))
        else:
            bot.send_message(message.from_user.id, "savatda hech nima yo'q")
    except:
        print('hatolik basket_detail')


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.enable_saving_states()
