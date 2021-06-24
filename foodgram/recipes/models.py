from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    class Status(models.TextChoices):
        BREAKFAST = 'Завтрак'
        LUNCH = 'Обед'
        DINNER = 'Ужин'
    
    class Colour(models.TextChoices):
        BREAKFAST = 'orange'
        LUNCH = 'green'
        DINNER = 'purple'

    name = models.CharField(
        max_length=7,
        choices=Status.choices,
        default=Status.DINNER,
        verbose_name='Название'
    )
    colour = models.CharField(
        max_length=6,
        choices=Colour.choices,
        default=Colour.DINNER,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        max_length=30,
        verbose_name='Короткое имя'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    units = models.CharField(max_length=200, verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Инградиент'
        verbose_name_plural = 'Инградиенты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Ингадиент'
    )
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Инградиент рецепта'
        verbose_name_plural = 'Инградиенты рецептов'

    def __str__(self):
        return (f'{self.ingredient.name} ' +
            f'({self.ingredient.units}) - {self.amount}')


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
    )
    description = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        RecipeIngredient,
        verbose_name='Инградиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги'
    )
    time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        default=0
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='users_favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='user_purchases',
        verbose_name='Рецепт'
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchase'
            )
        ]
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
