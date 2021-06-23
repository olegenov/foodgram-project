from django.shortcuts import get_object_or_404, redirect, render
from django.forms import ModelForm, Textarea

from .models import Ingredient, Recipe, RecipeIngredient, Tag
from .utils import count_purchase


class RecipeForm(ModelForm):
    def save(self, request, commit=True):
        tags = Tag.objects.all()
        purchase_count = count_purchase(request)
        recipe = None

        if commit:
            recipe = get_object_or_404(Recipe, pk=self.instance.pk)

        if not self.is_valid():
            return render(
                request,
                'recipes/new_recipe.html',
                {
                    'form': self,
                    'tags': tags,
                    'recipe': recipe,
                    'exists': commit,
                    'purchase_count': purchase_count,
                }
            )

        post_request = request.POST

        if not commit:
            recipe = Recipe.objects.create(
                name=post_request.get('name'),
                author=request.user,
                image=request.FILES.get('image'),
                description=post_request.get('description'),
                time=post_request.get('time')
            )
        else:
            recipe = get_object_or_404(Recipe, pk=self.instance.pk)

            if request.user != recipe.author:
                return redirect(
                    'recipe',
                    username=recipe.author.username,
                    recipe_id=recipe.pk
                )

            recipe.name = post_request.get('name')

            if request.FILES.get('image'):
                recipe.image = request.FILES.get('image')
            
            recipe.description = post_request.get('description')
            recipe.time = post_request.get('time')
            recipe.ingredients.clear()
        
        for key, value in request.POST.items():
            if key == 'tags':
                for tag_id in dict(request.POST).get('tags'):
                    recipe.tags.add(Tag.objects.get(pk=int(tag_id)))
            else:
                title = key.split('_')

                if title[0] == 'nameIngredient':
                    ingredient = Ingredient.objects.get(name=value)
                    amount = request.POST.get(f'valueIngredient_{title[1]}')
                    recipe_ingredient = RecipeIngredient.objects.create(
                        ingredient=ingredient,
                        amount=amount
                    )
                    recipe.ingredients.add(recipe_ingredient)

        return recipe


    class Meta:
        model = Recipe
        fields = ['name', 'description', 'image', 'time']
        widgets = {
            'description': Textarea(attrs={'cols': 50, 'rows': 10})
        }
