import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from FinBot.config import TOKEN
from telebot import TeleBot
from telebot import types
from bot_app.dictionary import dictionary
from bot_app.models import Profile
from bot_app.servises import new_password
from expenses_app.models import Expenses

bot = TeleBot(TOKEN)


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
        g = bot.send_message(chat_id=message.chat.id, text=dictionary['ask_gender'])
        bot.register_next_step_handler(g, ask_gender)


def ask_gender(message):
    if message.text == 'мужчина' or 'женщина':
        g = message.text
        t = bot.send_message(chat_id=message.chat.id, text=dictionary['ask_time_zone'])
        bot.register_next_step_handler(t, ask_time_zone, g)
    else:
        bot.send_message(chat_id=message.chat.id, text=dictionary['error_gender'])


def ask_time_zone(message, g):
    User.objects.create_user(username=message.chat.username, password=new_password())
    Profile.objects.create(external_id=message.chat.id,
                           user_id=User.objects.filter(username=message.chat.username).values('id')[0]['id'],
                           name=message.chat.username,
                           gender=g,
                           time_zone=message.text)
    bot.send_message(chat_id=message.chat.id, text=dictionary['add_profile'])
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
            item4 = types.KeyboardButton('Назад')
            murkup.add(item1, item2, item3, item4)

            bot.send_message(chat_id=message.chat.id, text='Какой тип статистики желаете получить?', reply_markup=murkup)
        elif message.text == 'Статистика за все время':
            get_history(message)


        elif message.text == 'Статистика за день':
            get_day_history(message)

        elif message.text == 'Назад':
            murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Статистика')
            item2 = types.KeyboardButton('Внести траты')
            item3 = types.KeyboardButton('Категории трат')
            item4 = types.KeyboardButton('Подсказки')
            murkup.add(item1, item2, item3, item4)

            bot.send_message(chat_id=message.chat.id, text='Назад', reply_markup=murkup)

        elif message.text == 'Внести траты':
            murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('продукты')
            item2 = types.KeyboardButton('кофе')
            item3 = types.KeyboardButton('обед')
            item4 = types.KeyboardButton('кафе')
            item5 = types.KeyboardButton('общественный транспорт')
            item6 = types.KeyboardButton('машина')
            item7 = types.KeyboardButton('телефон')
            item8 = types.KeyboardButton('книги')
            item9 = types.KeyboardButton('интернет')
            item10 = types.KeyboardButton('подписки')
            item11 = types.KeyboardButton('прочее')
            item12 = types.KeyboardButton('Назад')

            murkup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12)

            bot.send_message(chat_id=message.chat.id, text='Выберите категорию и введите сумму', reply_markup=murkup)
        elif message.text == 'Категории трат':
            bot.send_message(chat_id=message.chat.id, text=dictionary['category'])

        elif message.text == 'продукты':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)

        elif message.text == 'кофе':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)

        elif message.text == 'обед':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)

        elif message.text == 'кафе':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)

        elif message.text == 'общественный транспорт':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)

        elif message.text == 'машина':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)

        elif message.text == 'телефон':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)

        elif message.text == 'книги':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)

        elif message.text == 'интернет':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)

        elif message.text == 'подписки':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)

        elif message.text == 'прочее':
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, add_prodict, message.text)


def add_prodict(message, category):

    product_list = message.text.split()
    try:
        summ = int(product_list[1])
        product = product_list[0]
    except ValueError:
        summ = int(product_list[0])
        product = product_list[1]


    Expenses.objects.create(
        category=category,
        product=product,
        money=summ,
        user_id=User.objects.filter(username=message.chat.username).values('id')[0]['id']
    )
    bot.send_message(chat_id=message.chat.id, text='Расходы успешно добавлены!')


def get_history(message):
    expenses = Expenses.objects.filter(
        user_id=User.objects.filter(username=message.chat.username).values('id')[0]['id'])
    if expenses:
        res = ''
        total_exp = 0
        for i in expenses:
            res += f'{i.product}({i.category}): {i.money}руб.\n'
            total_exp += i.money
        bot.send_message(chat_id=message.chat.id, text=res)
        bot.send_message(chat_id=message.chat.id, text=f'Всего трат на сумму: {total_exp}')
    else:
        bot.send_message(chat_id=message.chat.id, text='Вы еще не добавили расходы')


def get_day_history(message):
    expenses = Expenses.objects.filter(
        user_id=User.objects.filter(username=message.chat.username).values('id')[0]['id'], created=datetime.date.today())
    if expenses:
        res = ''
        total_exp = 0
        for i in expenses:
            res += f'{i.product}({i.category}): {i.money}руб.\n'
            total_exp += i.money
        bot.send_message(chat_id=message.chat.id, text=res)
        bot.send_message(chat_id=message.chat.id, text=f'Всего трат на сумму: {total_exp}')
    else:
        bot.send_message(chat_id=message.chat.id, text='Сегодня Вы еще не добавили расходы')


