"""Настройки параметров.
"""
from enum import IntEnum


class Limits(IntEnum):
    # Максимальная длина email (User)
    MAX_LEN_EMAIL_FIELD = 200
    # Максимальная длина имени
    MAX_LEN_NAME = 150
    # Максимальная длина фамилии
    MAX_LAST_NAME = 150
    # Максимальная длинна ингридиента
    MAX_LEN_RECIPES_CHARFIELD = 200
    # Максимальная длинна имени метки
    MAX_LENGTH_TAG = 60
    # Максимальная длинна ссылки
    MAX_LENGTH_SLUG = 100
    # Максимальная длинна названия рецепта
    MAX_LENGTH_RECIPE = 255
    # Исключение для имени
    # EXCEPTION_RU = '[^а-яёА-ЯЁ -]+'
    # Исключение для фамилии
    # EXCEPTION_EN = '[^a-zA-Z -]+'
    # Максимальная длинна HEX
    MAX_LEN_HEX = 7
