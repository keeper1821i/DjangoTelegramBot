import datetime

from django.contrib.auth.models import User

from FinBot.config import bot
from bot_app.models import Profile
from expenses_app.models import Expenses
from plans_app.models import PlanExpenses
from telebot import types


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
    user_name = 'User' + str(message.chat.id)
    if message.text == 'Статистика за день':
        expenses = Expenses.objects.filter(
            user_id=User.objects.filter(username=user_name).values('id')[0]['id'],
            created__date=datetime.date.today())
        return expenses
    elif message.text == 'Статистика за все время':
        expenses = Expenses.objects.filter(
            user_id=User.objects.filter(username=user_name).values('id')[0]['id'])
        return expenses


def period_history(message, fd, sd):
    user_name = 'User' + str(message.chat.id)
    expenses = Expenses.objects.filter(
        user_id=User.objects.filter(username=user_name).values('id')[0]['id'],
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
    user_name = 'User' + str(message.chat.id)
    Expenses.objects.create(
            category=category,
            product=expenses,
            money=int(summ),
            user_id=User.objects.filter(username=user_name).values('id')[0]['id']
        )
    bot.send_message(chat_id=message.chat.id, text='Расходы успешно добавлены!')


def check_limit(message):
    limit = Profile.objects.filter(external_id=message.chat.id).values('limit')[0]['limit']
    month_limit = Profile.objects.filter(external_id=message.chat.id).values('month_limit')[0]['month_limit']
    if limit:
        user_name = 'User' + str(message.chat.id)
        expenses = Expenses.objects.filter(user_id=User.objects.filter(username=user_name).values('id')[0]['id'], created__date=datetime.date.today())
        total_exp = 0
        if expenses:
            for i in expenses:
                total_exp += i.money
        if total_exp > limit:
            bot.send_message(chat_id=message.chat.id, text=Profile.objects.filter(external_id=message.chat.id)
                             .values('day_text')[0]['day_text'])
        elif total_exp == limit:
            bot.send_message(chat_id=message.chat.id, text=f'Достигнут суточный лимит трат!')
    if month_limit:
        user_name = 'User' + str(message.chat.id)
        expenses = Expenses.objects.filter(user_id=User.objects.filter(username=user_name).values('id')[0]['id'], created__date=datetime.date.month)
        total_exp = 0
        if expenses:
            for i in expenses:
                total_exp += i.money
        if total_exp > month_limit:
            bot.send_message(chat_id=message.chat.id, text=Profile.objects.filter(external_id=message.chat.id)
                             .values('month_text')[0]['month_text'])
        elif total_exp == limit:
            bot.send_message(chat_id=message.chat.id, text=f'Достигнут месячный лимит трат!')


def get_plan(message):
    user_name = 'User' + str(message.chat.id)
    plan = PlanExpenses.objects.filter(
        user_id=User.objects.filter(username=user_name).values('id')[0]['id'])
    if plan:
        plan_list = ''
        for i in plan:
            plan_list += i.product + '\n'
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Назад \U0001F448')
        item2 = types.KeyboardButton('Купить из списка')
        murkup.add(item1, item2)
        bot.send_message(chat_id=message.chat.id, text=f'Вам необходимо купить: \n {plan_list} ', reply_markup=murkup)
    else:
        bot.send_message(chat_id=message.chat.id, text='Списка покупок еще нет:')

def bay_from_list(message):
    user_name = 'User' + str(message.chat.id)
    plan = PlanExpenses.objects.filter(
        user_id=User.objects.filter(username=user_name).values('id')[0]['id'])
    bay_list = []
    if plan:
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for i in plan:
            murkup.add(types.KeyboardButton(i.product))
            bay_list.append(i.product)
        murkup.add(types.KeyboardButton('Назад \U0001F448'))
        bot.send_message(chat_id=message.chat.id, text=f'Что купили?', reply_markup=murkup)

    else:
        bot.send_message(chat_id=message.chat.id, text='Списка покупок еще нет:')
    return bay_list


def add_product_in_bay_list(message, product):
    user_name = 'User' + str(message.chat.id)
    category = PlanExpenses.objects.filter(
        user_id=User.objects.filter(username=user_name).values('id')[0]['id'], product=product)
    print(category.values('category')[0]['category'])
    Expenses.objects.create(
            category=category.values('category')[0]['category'],
            product=product,
            money=int(message.text),
            user_id=User.objects.filter(username=user_name).values('id')[0]['id']
        )
    PlanExpenses.objects.filter(
        user_id=User.objects.filter(username=user_name).values('id')[0]['id'], product=product).delete()
    bay_from_list(message)
    bot.send_message(chat_id=message.chat.id, text='Расходы успешно добавлены!')

