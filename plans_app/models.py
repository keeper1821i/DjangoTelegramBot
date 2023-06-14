from django.contrib.auth.models import User
from django.db import models


class PlanExpenses(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(verbose_name='Наименование продукта', max_length=100)
    category = models.CharField(verbose_name='Категория трат', max_length=50)
