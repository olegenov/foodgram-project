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
    )
    colour = models.CharField(
        max_length=6,
        choices=Colour.choices,
        default=Colour.DINNER,
    )
    slug = models.SlugField(unique=True, max_length=30)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    units = models.CharField(max_length=200, verbose_name='Единицы измерения')

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    amount = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.ingredient.name} ({self.ingredient.units}) - {self.amount}'


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
    )
    description = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(RecipeIngredient)
    tags = models.ManyToManyField(Tag)
    time = models.PositiveIntegerField(verbose_name='Время приготовления', default=0)

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        unique_together = ['user', 'author']



class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='users_favorites'
    )

    class Meta:
        unique_together = ['user', 'recipe']


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='user_purchases'
    )
    
    class Meta:
        unique_together = ['user', 'recipe']
