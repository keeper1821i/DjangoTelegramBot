from django.db import models

class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='ID пользователя в телеграме')
    name = models.CharField(verbose_name='Имя пользователя', max_length=100)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
