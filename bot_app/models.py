from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    external_id = models.PositiveIntegerField(verbose_name='ID пользователя в телеграме')
    name = models.CharField(verbose_name='Имя пользователя', max_length=100)
    gender = models.CharField(max_length=10, verbose_name='пол', null=True)
    time_zone = models.CharField(verbose_name='Часовой пояс', max_length=3, null=True)
    token = models.CharField(verbose_name='Токен', max_length=65, null=True)
    limit = models.IntegerField(verbose_name='Суточный лимит', null=True)
    month_limit = models.IntegerField(verbose_name='Месячный лимит', null=True)
    day_text = models.CharField(verbose_name='екст лимита', max_length=100)
    month_text = models.CharField(verbose_name='екст лимита', max_length=100)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
