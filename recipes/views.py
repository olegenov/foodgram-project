from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from .forms import RecipeForm
from .models import (Favorite, Ingredient, Purchase, Recipe,
                     RecipeIngredient, Tag)
from .utils import count_purchase, generate_purchase, filter_tags


User = get_user_model()


def index(request):
    tags = Tag.objects.all()
    filtered_tags = filter_tags(request)
    active_tags = filtered_tags.get('active_tags')
    recipe_list = filtered_tags.get('recipe_list')
    paginator = Paginator(recipe_list, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    purchase_count = None

    if request.user.is_authenticated:
        purchase_count = count_purchase(request)

    return render(
        request,
        'index.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'active_tags': active_tags,
            'purchase_count': purchase_count,
        }
    )


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    ingredients = recipe.ingredients.all()
    tags = recipe.tags.all()
    purchase_count = None

    if request.user.is_authenticated:
        purchase_count = count_purchase(request)


    return render(
        request,
        'recipes/recipe_view.html',
        {
            'recipe': recipe,
            'ingredients': ingredients,
            'tags': tags,
            'purchase_count': purchase_count,
        }
    )


@login_required
def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    tags = Tag.objects.all()
    purchase_count = count_purchase(request)
    recipe = None

    if not form.is_valid():
        return render(
            request,
            'recipes/new_recipe.html',
            {
                'form': form,
                'tags': tags,
                'recipe': recipe,
                'exists': False,
                'purchase_count': purchase_count,
            }
        )

    recipe = form.save(request, commit=False)
    recipe.save()

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
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    tags = Tag.objects.all()
    purchase_count = count_purchase(request)

    if request.user != recipe.author:
        return redirect(
            'recipe',
            username=recipe.author.username,
            recipe_id=recipe.pk
        )
    
    if not form.is_valid():
        return render(
            request,
            'recipes/new_recipe.html',
            {
                'form': form,
                'tags': tags,
                'recipe': recipe,
                'exists': True,
                'purchase_count': purchase_count,
            }
        )

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    recipe = form.save(request)
    recipe.save()

    return redirect('recipe_view', username=username, recipe_id=recipe.pk)


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)

    if request.user != recipe.author:
        return redirect('index')

    recipe.delete()

    return redirect('profile_view', request.user.username)


def profile_view(request, username):
    profile = get_object_or_404(User, username=username)
    tags = Tag.objects.all()
    filtered_tags = filter_tags(request)
    active_tags = filtered_tags.get('active_tags')
    recipe_list = filtered_tags.get('recipe_list').filter(author=profile)
    paginator = Paginator(recipe_list, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    purchase_count = None

    if request.user.is_authenticated:
        purchase_count = count_purchase(request)

    return render(
        request,
        'recipes/profile_view.html',
        {
            'profile': profile,
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'active_tags': active_tags,
            'purchase_count': purchase_count,
        }
    )


@login_required
def follows(request):
    authors_list = User.objects.filter(
        pk__in=request.user.follower.all().values_list('author_id')
    )
    paginator = Paginator(authors_list, settings.PAGE_SIZE)
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
    favorite_list = Favorite.objects.filter(
        user=profile
    ).values_list('recipe_id')
    filtered_tags = filter_tags(request)
    active_tags = filtered_tags.get('active_tags')
    recipe_list = filtered_tags.get('recipe_list')
    recipe_list_filtered = recipe_list.filter(pk__in=favorite_list)
    paginator = Paginator(recipe_list_filtered, settings.PAGE_SIZE)
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
        }
    )


@login_required
def purchase(request):
    profile = request.user
    purchases = profile.purchases.all()
    recipes_list = Recipe.objects.filter(
        pk__in=purchases.values_list('recipe_id')
    )
    purchase_count = count_purchase(request)

    return render(
        request,
        'recipes/purchase.html',
        {'recipes_list': recipes_list, 'purchase_count': purchase_count}
    )


@login_required
def purchase_download(request):
    profile = request.user
    filename = 'purchase.txt'
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


@login_required
def purchase_delete(request, recipe_id):
    if Purchase.objects.filter(user=request.user, recipe__pk=recipe_id).exists():
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        get_object_or_404(Purchase, recipe=recipe, user=request.user).delete()

    return redirect('purchase')
