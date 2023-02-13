from django.contrib.auth.models import User
from django.db import models




class Expenses(models.Model):
    category = models.CharField(verbose_name='Категория трат', max_length=15)
    money = models.IntegerField(verbose_name='Потраченная сумма')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    product = models.CharField(verbose_name='Наименование продукта', max_length=100)
