from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'user' # Имя таблицы в базе данных в единственном !!! числе:
        verbose_name = 'Пользователя' # Имя будет отображаться в admin - панеле на русском языке в едиственном числе:
        verbose_name_plural = 'Пользователи'  # Имя будет отображаться в admin-панеле на русском языке во множественном числе:

    def __str__(self):
        return self.username # Возвращает правильное название созданной новой группы имени: