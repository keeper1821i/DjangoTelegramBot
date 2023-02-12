from django.contrib.auth.models import User
from django.db import models




class Expenses(models.Model):
    category = models.IntegerField(verbose_name='Категория трат')
    money = models.IntegerField(verbose_name='Потраченная сумма')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
