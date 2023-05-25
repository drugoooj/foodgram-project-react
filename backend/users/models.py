from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from core.enums import Limits


class User(AbstractUser):
    email = models.EmailField(
        'Email',
        max_length=Limits.MAX_LEN_EMAIL_FIELD.value,
        unique=True)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=Limits.MAX_LEN_NAME.value,
        validators=(RegexValidator(
            regex=r'[^!@$%^&]+',
            message='Введите имя без специальных символов.',
            code='invalid_first_name'),
        ),
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=Limits.MAX_LAST_NAME.value,
        validators=(RegexValidator(
            regex=r'[^!@$%^&]+',
            message='Введите фамилию без специальных символов.',
            code='invalid_last_name'),
        ),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.email
