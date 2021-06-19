from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import RecipeForm
from .models import (Favorite, Follow, Ingredient, Purchase, Recipe,
                     RecipeIngredient, Tag)


User = get_user_model()


def index(request):
    tags = Tag.objects.all()

    if request.GET.get('tags'):
        active_tags = request.GET.get('tags')
        tag_queryset = Tag.objects.filter(pk__in=active_tags)
        recipe_list = Recipe.objects.filter(
            tags__in=tag_queryset
        ).order_by('-pub_date').distinct()
    else:
        active_tags = '123'
        recipe_list = Recipe.objects.order_by('-pub_date').all()
    
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    purchase_count = None
    purchases = None
    favorites = None

    if request.user.is_authenticated:
        purchase_count = count_purchase(request)
        purchases = [
            purchase.recipe for purchase in request.user.purchases.all()
        ]
        favorites = [
            favorite.recipe for favorite in request.user.favorites.all()
        ]

    return render(
        request,
        'index.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'active_tags': active_tags,
            'purchase_count': purchase_count,
            'purchases': purchases,
            'favorites': favorites
        }
    )


def recipe_view(request, username, recipe_id):
    profile = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=profile)
    ingredients = recipe.ingredients.all()
    tags = recipe.tags.all()
    follow = None

    if request.user != profile:
        try:
            follow = Follow.objects.filter(
                user=request.user,
                author=profile
            ).exists()
        except:
            follow = None
    
    purchase_count = None
    in_purchase = None

    if request.user.is_authenticated:
        purchase_count = count_purchase(request)
        in_purchase = Purchase.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()


    return render(
        request,
        'recipes/recipe_view.html',
        {
            'recipe': recipe,
            'ingredients': ingredients,
            'tags': tags,
            'follow': follow,
            'purchase_count': purchase_count,
            'in_purchase': in_purchase
        }
    )


@login_required
def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    tags = Tag.objects.all()
    purchase_count = count_purchase(request)

    if not form.is_valid():
        return render(
            request,
            'recipes/new_recipe.html',
            {
                'form': form,
                'tags': tags,
                'exists': False,
                'purchase_count': purchase_count,
            }
        )

    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()

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

    return redirect(
        reverse(
            'profile_view',
            kwargs={
                'username': recipe.author.username
            }
        )
    )


@login_required
def recipe_edit(request, username, recipe_id):
    profile = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=profile)
    purchase_count = count_purchase(request)

    if request.user != recipe.author:
        return redirect('recipe', username=username, recipe_id=recipe.pk)

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    tags = Tag.objects.all()

    if not form.is_valid():
        return render(
            request,
            'recipes/new_recipe.html',
            {
                'form': form,
                'tags': tags,
                'recipe': recipe,
                'exists': True,
                'purchase_count': purchase_count
            }
        )
    
    form.save()
    recipe.ingredients.clear()

    for key, value in request.POST.items():
        if key == 'tags':
            recipe.tags.clear()
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

    return redirect('recipe_view', username=username, recipe_id=recipe.pk)


@login_required
def recipe_delete(request, username, recipe_id):
    profile = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=profile)

    if request.user != recipe.author:
        return redirect('index')

    recipe.delete()

    return redirect('profile_view', profile.username)


def profile_view(request, username):
    profile = get_object_or_404(User, username=username)
    tags = Tag.objects.all()

    if request.GET.get('tags'):
        active_tags = request.GET.get('tags')
        tag_queryset = Tag.objects.filter(pk__in=active_tags)
        recipe_list = profile.recipes.filter(
            tags__in=tag_queryset
        ).order_by('-pub_date').distinct()
    else:
        active_tags = '123'
        recipe_list = profile.recipes.order_by('-pub_date').all()
    
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    follow = None
    purchase_count = None
    purchases = None
    favorites = None

    if request.user.is_authenticated:
        purchase_count = count_purchase(request)
        purchases = [
            purchase.recipe for purchase in request.user.purchases.all()
        ]
        favorites = [
            favorite.recipe for favorite in request.user.favorites.all()
        ]

    if request.user != profile:
        try:
            follow = Follow.objects.get(user=request.user, author=profile)
        except:
            follow = None

    return render(
        request,
        'recipes/profile_view.html',
        {
            'profile': profile,
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'active_tags': active_tags,
            'follow': follow,
            'purchase_count': purchase_count,
            'purchases': purchases,
            'favorites': favorites
        }
    )


@login_required
def follows(request):
    authors_list = User.objects.filter(following__user=request.user)
    paginator = Paginator(authors_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    purchase_count = count_purchase(request)

    return render(
        request,
        'recipes/follows.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'purchase_count': purchase_count
        }
    )


@login_required
def favorites(request):
    profile = request.user
    favorite = Favorite.objects.filter(user=profile)
    favorite_list = [favorite.recipe.pk for favorite in favorite]
    recipe_list = Recipe.objects.filter(pk__in=favorite_list)
    purchases = [purchase.recipe for purchase in request.user.purchases.all()]
    favorites = [favorite.recipe for favorite in request.user.favorites.all()]

    if request.GET.get('tags'):
        active_tags = request.GET.get('tags')
        tag_queryset = Tag.objects.filter(pk__in=active_tags)
        recipe_list_filtered = recipe_list.filter(
            tags__in=tag_queryset
        ).order_by('-pub_date').distinct()
    else:
        active_tags = '123'
        recipe_list_filtered = recipe_list.order_by('-pub_date').all()

    paginator = Paginator(recipe_list_filtered, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    purchase_count = count_purchase(request)

    return render(
        request,
        'recipes/favorites.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'active_tags': active_tags,
            'purchase_count': purchase_count,
            'purchases': purchases,
            'favorites': favorites
        }
    )


@login_required
def purchase(request):
    profile = request.user
    purchases = profile.purchases.all()
    recipes_list = [purchase.recipe for purchase in purchases]
    purchase_count = count_purchase(request)

    return render(
        request,
        'recipes/purchase.html',
        {'recipes_list': recipes_list, 'purchase_count': purchase_count}
    )


@login_required
def purchase_download(request):
    profile = request.user
    filename = "purchase.txt"
    content = generate_purchase(profile)

    if content == '':
        return redirect(
            'purchase'
        )

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename
    )
    return response


def generate_purchase(profile):
    purchases = profile.purchases.all()
    recipes_list = [purchase.recipe for purchase in purchases]
    ingredients_list = {}

    for recipe in recipes_list:
        for ingredient in recipe.ingredients.all():
            if ingredient.ingredient.name in ingredients_list:
                ingredients_list[
                    ingredient.ingredient.name
                ][0] += ingredient.amount
            else:
                ingredients_list.update(
                    {
                        f'{ingredient.ingredient.name}': [
                            ingredient.amount,
                            ingredient.ingredient.units
                        ]
                    }
                )

    items = ingredients_list.items()

    purchase = '\n'.join(
        [
            f'{key} ({value[1]}) — {value[0]}' for key, value in items
        ]
    )

    return purchase


@login_required
def purchase_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    Purchase.objects.get(recipe=recipe).delete()

    return redirect('purchase')


def count_purchase(request):
    count = Purchase.objects.filter(user=request.user).count()

    return count


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
