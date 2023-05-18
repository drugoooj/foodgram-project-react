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
