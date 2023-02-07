from django.db import models

from bot_app.models import Profile


class Expenses(models.Model):
    category = models.IntegerField(verbose_name='Категория трат')
    money = models.IntegerField(verbose_name='Потраченная сумма')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
