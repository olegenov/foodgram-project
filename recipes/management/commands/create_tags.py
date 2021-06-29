from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Create tags'

    def handle(self, *args, **options):
        tags = {'Breakfast': 'Завтрак', 'Lunch': 'Обед', 'Dinner': 'Ужин'}
        colours = {'Breakfast': 'orange', 'Lunch': 'green', 'Dinner': 'purple'}
        for tag, value in tags.items():
            if not Tag.objects.filter(name=Tag.Status(value)).exists():
                Tag.objects.get_or_create(
                    name=Tag.Status(value),
                    colour=colours.get(tag),
                    slug=tag.lower()
                )
