import datetime

from django.contrib.auth.models import User

from FinBot.config import bot
from expenses_app.models import Expenses


def get_history(message):
    expenses = history(message)
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


def history(message):
    if message.text == 'Статистика за день':
        expenses = Expenses.objects.filter(
            user_id=User.objects.filter(username=message.chat.username).values('id')[0]['id'],
            created=datetime.date.today())
        return expenses
    elif message.text == 'Статистика за все время':
        expenses = Expenses.objects.filter(
            user_id=User.objects.filter(username=message.chat.username).values('id')[0]['id'])
        return expenses


def period_history(message, fd, sd):
    expenses = Expenses.objects.filter(
        user_id=User.objects.filter(username=message.chat.username).values('id')[0]['id'],
        created__gte=fd, created__lte=sd)
    if expenses:
        res = ''
        total_exp = 0
        for i in expenses:
            res += f'{i.product}({i.category}): {i.money}руб.\n'
            total_exp += i.money
        bot.send_message(chat_id=message.chat.id, text=res)
        bot.send_message(chat_id=message.chat.id, text=f'Всего трат на сумму: {total_exp}')
    else:
        bot.send_message(chat_id=message.chat.id, text='За выбранный период у Вас не было расходов')


def add_product(message, category, expenses, summ):
    Expenses.objects.create(
            category=category,
            product=expenses,
            money=int(summ),
            user_id=User.objects.filter(username=message.chat.username).values('id')[0]['id']
        )
    bot.send_message(chat_id=message.chat.id, text='Расходы успешно добавлены!')