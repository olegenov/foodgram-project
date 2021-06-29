from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Favorite, Follow, Ingredient, Purchase, Recipe


User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='pk'
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='pk'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('user',)
        model = Follow


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='pk'
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='pk'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('user',)
        model = Favorite


class PurchaseSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='pk'
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='pk'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('user',)
        model = Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = ('user',)
        model = Recipe
