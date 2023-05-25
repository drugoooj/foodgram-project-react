from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import F, Q

from core.enums import Limits

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=Limits.MAX_LEN_RECIPES_CHARFIELD.value,
        validators=[
            RegexValidator(
                regex=r'[^!@$%^&]+',
                message='Введите название без спец символов.'
            )
        ]
    )
    measurement_unit = models.CharField(
        'Единица измерения ингредиента',
        max_length=Limits.MAX_LEN_RECIPES_CHARFIELD.value)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Tag(models.Model):
    name = models.CharField(
        'Имя',
        max_length=Limits.MAX_LENGTH_TAG.value,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'[^!@$%^&]+',
                message='Введите название без спец символов.'
            )
        ]
    )
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=Limits.MAX_LEN_HEX.value,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{3,6})$',
                message='Введенное значение не является цветом в формате HEX!'
            )
        ]
    )
    slug = models.SlugField(
        'Ссылка',
        max_length=Limits.MAX_LENGTH_SLUG.value,
        unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор')
    name = models.CharField(
        'Название рецепта',
        max_length=Limits.MAX_LENGTH_RECIPE.value)
    image = models.ImageField(
        'Изображение рецепта',
        upload_to='static/recipe/',
        blank=True,
        null=True)
    text = models.TextField(
        'Описание рецепта')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[validators.MinValueValidator(
            1, message='Мин. время приготовления 1 минута'), ])
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name=_('Recipe')
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Ingredient'),
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=(
            validators.MinValueValidator(
                1, message='Мин. количество ингридиентов 1'),),
        verbose_name='Количество',)

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient')]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')
    created = models.DateTimeField(
        'Дата подписки',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='user_cannot_subscribe_to_self'
            )
        ]

    def __str__(self):
        return f'Пользователь {self.user} -> автор {self.author}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Recipe')
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в избранные.'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Recipe')
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-id']

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в покупки.'
