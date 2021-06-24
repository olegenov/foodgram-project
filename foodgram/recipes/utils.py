from .models import Purchase, Recipe, Tag


def get_all_tags():
    tags = Tag.objects.all().values_list('pk')
    tags_list = [str(value[0]) for value in tags]

    return ''.join(tags_list)


def count_purchase(request):
    count = Purchase.objects.filter(user=request.user).count()

    return count


def generate_purchase(profile):
    purchases = profile.purchases.all()
    recipes_list = Recipe.objects.filter(
        pk__in=purchases.values_list('recipe_id')
    )
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


def filter_tags(request):
    if request.GET.get('tags'):
        active_tags = request.GET.get('tags')
        tag_queryset = Tag.objects.filter(pk__in=active_tags)
        recipe_list = Recipe.objects.filter(
            tags__in=tag_queryset
        ).order_by('-pub_date').distinct()
    else:
        active_tags = get_all_tags()
        recipe_list = Recipe.objects.order_by('-pub_date').all()
    
    return {'recipe_list': recipe_list, 'active_tags': active_tags}
