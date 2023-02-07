from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from FinBot.config import TOKEN
from telebot import TeleBot
from bot_app.models import Profile
from bot_app.dictionary import dictionary
from bot_app.servises import new_password

bot = TeleBot(TOKEN)


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.infinity_polling()  # Бесконечный цикл бота


@bot.message_handler(commands=['start'])
def start_message(message) -> None:
    """Стартовое сообщение"""
    bot.send_message(chat_id=message.chat.id, text=dictionary['started_message'])
    if not Profile.objects.filter(external_id=message.chat.id):
        User.objects.create_user(username=message.chat.username, password=new_password())
        Profile.objects.create(name=message.chat.first_name, external_id=message.chat.id,
                               user_id=User.objects.all().last().id)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(chat_id=message.chat.id, text=dictionary['help_message'])


@bot.message_handler(commands=['categories'])
def help_message(message):
    bot.send_message(chat_id=message.chat.id, text=dictionary['category'])

