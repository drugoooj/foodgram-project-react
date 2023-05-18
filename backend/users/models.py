from core.enums import Limits
from core.validators import OneOfTwoValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        'Email',
        max_length=Limits.MAX_LEN_EMAIL_FIELD.value,
        unique=True)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=Limits.MAX_LEN_NAME.value,
        validators=(OneOfTwoValidator(
            first_regex='[^а-яёА-ЯЁ -]+',
            second_regex='[^a-zA-Z -]+',
            field='Имя'),
        ),
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=Limits.MAX_LAST_NAME.value,
        validators=(OneOfTwoValidator(
            first_regex='[^а-яёА-ЯЁ -]+',
            second_regex='[^a-zA-Z -]+',
            field='Фамилия'),
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
