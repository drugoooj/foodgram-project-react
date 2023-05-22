from re import compile
from typing import Optional
from django.core.exceptions import ValidationError


class OneOfTwoValidator:
    """Проверяет введённую строку регулярными выражениями.

    Проверяет, соответствует ли введённая строка двум регулярным выражениям.
    Разрешенно не более, чем одно соответствие.
    Если регулярные выражения не переданы при вызове, применяются выражения
    по умолчанию. По умолчанию, во избежание коллизий,
    строка может состоять только из латинских или только из русских букв.

    Attributes:
        first_regex (str):
            Первый вариант допустимого регулярного выражения для сравнения
            со значением. По умолчанию - только русские буквы.
        second_regex (str):
            Второй вариант допустимого регулярного выражения для сравнения
            со значением. По умолчанию - только латинские буквы.
        field (str):
            Название проверяемого поля.

        Raises:
            ValidationError:
                Переданное значение содержит символы, разрешённые обоими
                регулярными выражениями.
    """
    first_regex = r'[^а-яёА-ЯЁ]+'
    second_regex = r'[^a-zA-Z]+'
    field = 'Переданное значение'
    message = '<%s> на разных языках либо содержит не только буквы.'

    def __init__(
        self,
        first_regex: Optional[str] = None,
        second_regex: Optional[str] = None,
        field: Optional[str] = None,
    ) -> None:
        if first_regex is not None:
            self.first_regex = first_regex
        if second_regex is not None:
            self.second_regex = second_regex
        if field is not None:
            self.field = field
        self.message = f'\n{self.field} {self.message}\n'

        self.first_regex = compile(self.first_regex)
        self.second_regex = compile(self.second_regex)

    def __call__(self, value: str) -> None:
        if self.first_regex.search(value) and self.second_regex.search(value):
            raise ValidationError(self.message % value)
