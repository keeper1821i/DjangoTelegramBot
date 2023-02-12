import re

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from FinBot.config import TOKEN
from telebot import TeleBot
from telebot import types
# from bot_app.models import Profile
from bot_app.dictionary import dictionary
from bot_app.models import Profile
from bot_app.servises import new_password

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
            item1 = types.KeyboardButton('Статистика за день ')
            item2 = types.KeyboardButton('Статистика за месяц')
            item3 = types.KeyboardButton('Статистика за период')
            item4 = types.KeyboardButton('Назад')
            murkup.add(item1, item2, item3, item4)

            bot.send_message(chat_id=message.chat.id, text='Статистика', reply_markup=murkup)

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


