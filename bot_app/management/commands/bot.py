import datetime
import time
import telebot_calendar
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from telebot import TeleBot, types
from telebot.types import ReplyKeyboardRemove

from FinBot.config import TOKEN
from bot_app.dictionary import category_list, dictionary
from bot_app.management.services import get_history, period_history, add_product, check_limit, get_plan, bay_from_list, add_product_in_bay_list
from bot_app.models import Profile
from plans_app.models import PlanExpenses

bot = TeleBot(TOKEN, threaded=False)
calendar_0 = telebot_calendar.Calendar(language=telebot_calendar.RUSSIAN_LANGUAGE)
calendar_1_callback = telebot_calendar.CallbackData("calendar_1", "action", "year", "month", "day")
f_date = None

class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        while True:
            try:
                bot.polling(none_stop=True)  # Бесконечный цикл бота
            except Exception as e:
                print(e)
                time.sleep(3)





@bot.message_handler(commands=['start'])
def start_message(message) -> None:
    """Стартовое сообщение"""
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Статистика')
    item2 = types.KeyboardButton('Внести траты')
    item3 = types.KeyboardButton('Категории трат')
    item4 = types.KeyboardButton('Подсказки')
    item5 = types.KeyboardButton('Что нужно купить')
    item6 = types.KeyboardButton("Личный кабинет")
    murkup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(chat_id=message.chat.id, text=dictionary['started_message'], reply_markup=murkup)
    user_name = 'User' + str(message.chat.id)
    if not User.objects.filter(username=user_name):
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
    user_name = 'User' + str(message.chat.id)
    User.objects.create_user(username=user_name, password='12345678')
    Profile.objects.create(external_id=message.chat.id,
                           user_id=User.objects.filter(username=user_name).values('id')[0]['id'],
                           name=user_name,
                           gender=g,
                           time_zone=message.text,
                           limit='500',
                           month_limit='15000',
                           day_text='Внимание! Вы превысили установленный дневной лимит трат.',
                           month_text='Внимание! Вы превысили установленный месячный лимит трат.')
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Статистика')
    item2 = types.KeyboardButton('Внести траты')
    item3 = types.KeyboardButton('Категории трат')
    item4 = types.KeyboardButton('Подсказки')
    item5 = types.KeyboardButton('Что нужно купить')
    item6 = types.KeyboardButton("Личный кабинет")
    murkup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(chat_id=message.chat.id, text=dictionary['add_profile'], reply_markup=murkup)
    bot.register_next_step_handler(message, bot_message)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    user_name = 'User' + str(message.chat.id)
    plan = PlanExpenses.objects.filter(
        user_id=User.objects.filter(username=user_name).values('id')[0]['id'])
    bay_list = []
    if plan:
        for i in plan:
            bay_list.append(i.product)
    if message.chat.type == 'private':
        if message.text == 'Подсказки':
            murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Контакты')
            item2 = types.KeyboardButton('О боте')
            item3 = types.KeyboardButton('Как добавить покупку')
            item4 = types.KeyboardButton('Использование статистики')
            item5 = types.KeyboardButton('Будущие траты')
            item6 = types.KeyboardButton('Личный кабинет')
            item7 = types.KeyboardButton('Назад \U0001F448')
            murkup.add(item1, item2, item3, item4, item5, item6, item7)

            bot.send_message(chat_id=message.chat.id, text='О чем хотите узнать?',
                             reply_markup=murkup)

        elif message.text == 'Личный кабинет':
            bot.send_message(chat_id=message.chat.id, text='Помимо самого телеграмм бота вам доступен личный кабинет\n '
                                                           'пользователя. Чтобы попасть в него, на главном меню нажмите'
                                                           ' "Личный кабинет". Перейдите по ссылке и авторизуйтесь с '
                                                           'помощью самого телеграмма.В личном кабинете вам доступны '
                                                           'виджеты статистики, доступен раздел с полным списком трат. '
                                                           'Так же реализована функция лимита трат. Нажмите на иконку '
                                                           'аватарки справа вверху и перейдите в настройки. Вам '
                                                           'доступны дневные и месячные лимиты трат. Задайте сумму и текст '
                                                           'предупреждения для каждого типа и телеграмм бот при '
                                                           'добавлении новой траты будет предупреждать вас о '
                                                           'существующем лимите.')
        elif message.text == 'Контакты':
            bot.send_message(chat_id=message.chat.id, text='Вы всегда можете написать нам с предложением или вашей '
                                                           'проблемой на наш почтовый адрес - info@finbotpay.ru\n '
                                                           'Так же вы можете вступить в нашу группу в '
                                                           'VK - https://vk.com/finbotpay')

        elif message.text == 'О боте':
            bot.send_message(chat_id=message.chat.id, text='FinBot - это телеграмм бот, который поможет вам фиксировать '
                                                           'все ваши ежедневные покупки, вести статистику, управлять '
                                                           'планированием будущих покупок и многое другое.')

        elif message.text == 'Как добавить покупку':
            bot.send_message(chat_id=message.chat.id, text='Для того, чтобы добавить покупку вам нужно выбрать '
                                                           '"Внести траты", далее бот предложит вам выбрать категорию. '
                                                           'После того как выбрали категорию, введите числовое значение '
                                                           'стоимости покупки. После этого ваша покупка будет '
                                                           'зафиксирована и доступна в разделе "Статистика".')

        elif message.text == 'Использование статистики':
            bot.send_message(chat_id=message.chat.id, text='Все ваши покупки фиксируются в боте и доступны в разделе '
                                                           '"Статистика". В разделе доступны три варианта статистики - '
                                                           'За день, За все время и возможность получить статистику за '
                                                           'нужный вам период. При выборе статистики за нужный вам '
                                                           'период бот предложит выбрать на календаре сначала дату '
                                                           'начала, а потом дату конца периода. После этого вы получите '
                                                           'список покупок за нужный вам период.')

        elif message.text == 'Будущие траты':
            bot.send_message(chat_id=message.chat.id, text='Раздел находится в разработке')

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

        elif message.text == 'Что нужно купить':
            get_plan(message)

        elif message.text == 'Статистика за день':
            get_history(message)

        elif message.text == 'Назад \U0001F448':
            murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Статистика')
            item2 = types.KeyboardButton('Внести траты')
            item3 = types.KeyboardButton('Категории трат')
            item4 = types.KeyboardButton('Подсказки')
            item5 = types.KeyboardButton('Что нужно купить')
            item6 = types.KeyboardButton("Личный кабинет")
            murkup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(chat_id=message.chat.id, text='Выберите следующее действие', reply_markup=murkup)

        elif message.text == 'Внести траты':
            check_limit(message)
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

            murkup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item14, item13, item12)

            bot.send_message(chat_id=message.chat.id, text='Выберите категорию и введите сумму', reply_markup=murkup)
        elif message.text == 'Категории трат':
            bot.send_message(chat_id=message.chat.id, text=dictionary['category'])

        elif message.text in category_list:
            bot.send_message(chat_id=message.chat.id, text=dictionary['add_product'])
            bot.register_next_step_handler(message, asc_expenses, message.text)

        elif message.text == 'Статистика за период':
            bot.send_message(chat_id=message.chat.id, text='Дата начала периода')
            show_calendar(message)

        elif message.text == 'Купить из списка':
            bay_from_list(message)

        elif message.text in bay_list:
            bot.send_message(chat_id=message.chat.id, text='Сколько потратили?')
            bot.register_next_step_handler(message, add_product_in_bay_list, message.text)

        elif message.text == "Личный кабинет":
            murkup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Личный кабинет", url='http://finbotpay.ru/#/')

            murkup.add(item1)

            bot.send_message(chat_id=message.chat.id, text='Нажмите для перехода в личный кабинет', reply_markup=murkup)


def asc_expenses(message, category):
    if message.text == 'Назад \U0001F448':
        bot.register_next_step_handler(message, bot_message)
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Статистика')
        item2 = types.KeyboardButton('Внести траты')
        item3 = types.KeyboardButton('Категории трат')
        item4 = types.KeyboardButton('Подсказки')
        item5 = types.KeyboardButton('Что нужно купить')
        item6 = types.KeyboardButton("Личный кабинет")
        murkup.add(item1, item2, item3, item4, item5, item6)

        bot.send_message(chat_id=message.chat.id, text='Выберите следующее действие', reply_markup=murkup)
    else:
        bot.send_message(chat_id=message.chat.id, text='Сколько потратили?')
        bot.register_next_step_handler(message, asc_summ, category, message.text)

def asc_summ(message, category, expenses):
    if message.text == 'Назад \U0001F448':
        bot.register_next_step_handler(message, bot_message)
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Статистика')
        item2 = types.KeyboardButton('Внести траты')
        item3 = types.KeyboardButton('Категории трат')
        item4 = types.KeyboardButton('Подсказки')
        item5 = types.KeyboardButton('Что нужно купить')
        item6 = types.KeyboardButton("Личный кабинет")
        murkup.add(item1, item2, item3, item4, item5, item6)

        bot.send_message(chat_id=message.chat.id, text='Выберите следующее действие', reply_markup=murkup)
    else:

        bot.send_message(chat_id=message.chat.id, text='Обработка.....')
        try:
            if isinstance(int(message.text), int) and int(message.text) > 0:
                add_product(message, category, expenses, message.text)
        except ValueError:
            bot.send_message(chat_id=message.chat.id, text='Ошибка формата, введите число')
            bot.register_next_step_handler(message, asc_summ, category, message.text)



def show_calendar(message):
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
    global f_date
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    date = calendar_0.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )

    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"Вы выбрали {date.strftime('%d.%m.%y')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        d = date
        first_date(call.message, d)
    elif action == "CANCEL":
        f_date = None
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Статистика за день')
        item2 = types.KeyboardButton('Статистика за все время')
        item3 = types.KeyboardButton('Статистика за период')
        item4 = types.KeyboardButton('Назад \U0001F448')
        murkup.add(item1, item2, item3, item4)
        bot.send_message(
            chat_id=call.from_user.id,
            text="Отмена ввода",
            reply_markup=murkup,
        )


def first_date(message, d):
    global f_date
    sd = None
    if f_date:
        fd = f_date
        sd = d
        bot.send_message(chat_id=message.chat.id, text=f"Статистика за период {fd.strftime('%d.%m.%y')} - {sd.strftime('%d.%m.%y')}")
        f_date = None
        period_history(message, fd, sd)
        murkup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Статистика')
        item2 = types.KeyboardButton('Внести траты')
        item3 = types.KeyboardButton('Категории трат')
        item4 = types.KeyboardButton('Подсказки')
        item5 = types.KeyboardButton('Что нужно купить')
        item6 = types.KeyboardButton("Личный кабинет")
        murkup1.add(item1, item2, item3, item4, item5, item6)
        bot.send_message(chat_id=message.chat.id, text='Выберите следующее действие', reply_markup=murkup1)
        bot.register_next_step_handler(message, bot_message)
    else:
        f_date = d
        bot.send_message(chat_id=message.chat.id, text='Дата окончания периода')
        show_calendar(message)
