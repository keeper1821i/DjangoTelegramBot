from django.core.management.base import BaseCommand
from FinBot.config import TOKEN
from telebot import TeleBot
from bot_app.models import Profile
from bot_app.dictionary import dictionary

bot = TeleBot(TOKEN)


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.infinity_polling()  # Бесконечный цикл бота


@bot.message_handler(commands=['start', 'help'])
def start_message(message) -> None:
    print(123)
    """Стартовое сообщение"""
    bot.send_message(chat_id=message.chat.id, text=dictionary['started_message'])
    if not Profile.objects.filter(external_id=message.chat.id):
        Profile.objects.create(name=message.chat.username, external_id=message.chat.id)
