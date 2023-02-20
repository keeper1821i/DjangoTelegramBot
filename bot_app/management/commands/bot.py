import datetime
import re

import telebot_calendar
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from telebot import TeleBot, types
from telebot.types import ReplyKeyboardRemove

from FinBot.config import TOKEN
from bot_app.dictionary import category_list, dictionary
from bot_app.management.services import get_history, period_history
from bot_app.models import Profile
from expenses_app.models import Expenses

bot = TeleBot(TOKEN, threaded=False)
calendar_0 = telebot_calendar.Calendar(language=telebot_calendar.RUSSIAN_LANGUAGE)
calendar_1_callback = telebot_calendar.CallbackData("calendar_1", "action", "year", "month", "day")
f_date = None

class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.polling(none_stop=True)  # Бесконечный цикл бота



@bot.message_handler(commands=['start'])
def start_message(message) -> None:
    """Стартовое сообщение"""
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Статистика')
    item2 = types.KeyboardButton('Внести траты')
    item3 = types.KeyboardButton('Категории трат')
    item4 = types.KeyboardButton('Подсказки')
    murkup.add(item1, item2, item3, item4)
    bot.send_message(chat_id=message.chat.id, text=dictionary['started_message'], reply_markup=murkup)
    if not User.objects.filter(username=message.chat.username):
        murkup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Мужской')
        item2 = types.KeyboardButton('Женский')
        murkup1.add(item1, item2)
        g = bot.send_message(chat_id=message.chat.id, text=dictionary['ask_gender'], reply_markup=murkup1)
        bot.register_next_step_handler(g, ask_gender)
    else:
        bot.register_next_step_handler(message, bot_message)


def ask_gender(message):
    g = message.text
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('+2')
    item2 = types.KeyboardButton('+3')
    item3 = types.KeyboardButton('+4')
    item4 = types.KeyboardButton('+5')
    item5 = types.KeyboardButton('+6')
    item6 = types.KeyboardButton('+7')
    item7 = types.KeyboardButton('+8')
    item8 = types.KeyboardButton('+9')
    item9 = types.KeyboardButton('+10')
    item10 = types.KeyboardButton('+11')
    item11 = types.KeyboardButton('+12')
    murkup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11)
    t = bot.send_message(chat_id=message.chat.id, text=dictionary['ask_time_zone'], reply_markup=murkup)
    bot.register_next_step_handler(t, ask_time_zone, g)


def ask_time_zone(message, g):
    User.objects.create_user(username=message.chat.username, password='12345678')
    Profile.objects.create(external_id=message.chat.id,
                           user_id=User.objects.filter(username=message.chat.username).values('id')[0]['id'],
                           name=message.chat.username,
                           gender=g,
                           time_zone=message.text)
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Статистика')
    item2 = types.KeyboardButton('Внести траты')
    item3 = types.KeyboardButton('Категории трат')
    item4 = types.KeyboardButton('Подсказки')
    murkup.add(item1, item2, item3, item4)
    bot.send_message(chat_id=message.chat.id, text=dictionary['add_profile'], reply_markup=murkup)
    bot.register_next_step_handler(message, bot_message)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Подсказки':
            bot.send_message(chat_id=message.chat.id, text=dictionary['help_message'])
        elif message.text == 'Статистика':
            murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Статистика за день')
            item2 = types.KeyboardButton('Статистика за все время')
            item3 = types.KeyboardButton('Статистика за период')
            item4 = types.KeyboardButton('Назад \U0001F448')
            murkup.add(item1, item2, item3, item4)

            bot.send_message(chat_id=message.chat.id, text='Какой тип статистики желаете получить?', reply_markup=murkup)
        elif message.text == 'Статистика за все время':
            get_history(message)

        elif message.text == 'Статистика за день':
            get_history(message)

        elif message.text == 'Назад \U0001F448':
            murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Статистика')
            item2 = types.KeyboardButton('Внести траты')
            item3 = types.KeyboardButton('Категории трат')
            item4 = types.KeyboardButton('Подсказки')
            murkup.add(item1, item2, item3, item4)

            bot.send_message(chat_id=message.chat.id, text='Назад \U0001F448', reply_markup=murkup)

        elif message.text == 'Внести траты':
            murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Продукты \U0001F353')
            item2 = types.KeyboardButton('Проезд \U0001F68C')
            item3 = types.KeyboardButton('Подарки \U0001F381')
            item4 = types.KeyboardButton('Платежи, комисии \U0001F4B0')
            item5 = types.KeyboardButton('Отдых и развлечения \U0001F3D6')
            item6 = types.KeyboardButton('Образование \U0001F4D7')
            item7 = types.KeyboardButton('Машина \U0001F697')
            item8 = types.KeyboardButton('Кафе и рестораны \U00002615')
            item9 = types.KeyboardButton('Здоровье и фитнес \U0001F3C3')
            item10 = types.KeyboardButton('Забота о себе \U0001F485')
            item11 = types.KeyboardButton('Дети \U0001F47C')
            item12 = types.KeyboardButton('Назад \U0001F448')
            item13 = types.KeyboardButton('Покупка одежды, техника \U0001F5A5')
            item14 = types.KeyboardButton('Другие расходы \U0001F4CC')

            murkup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13, item14)

            bot.send_message(chat_id=message.chat.id, text='Выберите категорию и введите сумму', reply_markup=murkup)
        elif message.text == 'Категории трат':
            bot.send_message(chat_id=message.chat.id, text=dictionary['category'])

        elif message.text in category_list:
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_product, message.text)

        elif message.text == 'Статистика за период':
            global f_date
            f_date = None
            now = datetime.datetime.now()  # Get the current date
            bot.send_message(
                chat_id=message.chat.id,
                text="Выберите дату",
                reply_markup=calendar_0.create_calendar(
                    name=calendar_1_callback.prefix,
                    year=now.year,
                    month=now.month,  # Specify the NAME of your calendar
                ),
            )
            bot.register_next_step_handler(message, statistic)


def add_product(message, category):
    temp = re.compile("(\w+?)(\d+)")
    res = re.findall(temp, message.text)
    print(res)
    print(message.text)
    product_list = message.text.split()
    if len(product_list) == 2:
        try:
            summ = int(product_list[1])
            product = product_list[0]
        except ValueError:
            try:
                summ = int(product_list[0])
                product = product_list[1]
            except ValueError:
                mess = bot.send_message(chat_id=message.chat.id, text='Введите расходы в форме: "Хлеб 100"')
                bot.register_next_step_handler(mess, add_product, category)
        Expenses.objects.create(
            category=category,
            product=product,
            money=summ,
            user_id=User.objects.filter(username=message.chat.username).values('id')[0]['id']
        )
        bot.send_message(chat_id=message.chat.id, text='Расходы успешно добавлены!')
    else:
        mess = bot.send_message(chat_id=message.chat.id, text='Введите расходы в форме: "Хлеб 100"')
        bot.register_next_step_handler(mess, add_product, category)


def statistic(message):
    bot.send_message(chat_id=message.chat.id, text='Выберите дату')
    now = datetime.datetime.now()  # Get the current date
    bot.send_message(
        chat_id=message.chat.id,
        text="Выберите дату",
        reply_markup=calendar_0.create_calendar(
            name=calendar_1_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix))

def callback_inline(call):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar_0.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"Вы выбрали {date.strftime('%d.%m.%Y')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1_callback}: Day: {date.strftime('%d.%m.%Y')}")
        d = date
        first_date(call.message, d)
        print(d)
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1_callback}: Cancellation")


def first_date(message, d):
    global f_date
    sd = None
    if f_date:
        fd = f_date
        sd = d
        bot.send_message(chat_id=message.chat.id, text=f'Статистика за период {fd} - {sd}')
        f_date = None
        period_history(message, fd, sd)
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Статистика')
        item2 = types.KeyboardButton('Внести траты')
        item3 = types.KeyboardButton('Категории трат')
        item4 = types.KeyboardButton('Подсказки')
        murkup.add(item1, item2, item3, item4)
        bot.send_message(chat_id=message.chat.id, text='Выберите следующее действие', reply_markup=murkup)
        bot.register_next_step_handler(message, bot_message)
    else:
        f_date = d
        statistic(message)

        # bot.register_next_step_handler(message, bot_message)