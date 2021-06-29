from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, Purchase, Recipe,
                     RecipeIngredient, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'colour', 'slug') 
    search_fields = ('name',) 
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'units')
    search_fields = ('name',) 
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'amount') 
    search_fields = ('name',) 
    empty_value_display = '-пусто-'


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'pub_date', 'author', 'image',
                    'description', 'time') 
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    inlines = [
        IngredientInline,
        TagInline,
    ]
    exclude = ('ingredients', 'tags')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author') 
    search_fields = ('user', 'author') 
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe') 
    search_fields = ('user',) 
    empty_value_display = '-пусто-'


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe') 
    search_fields = ('user',) 
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
