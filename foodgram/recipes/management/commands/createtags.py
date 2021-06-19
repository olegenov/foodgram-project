from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Create tags'

    def handle(self, *args, **options):
        pk = 1
        tags = {'Breakfast': 'Завтрак', 'Lunch': 'Обед', 'Dinner': 'Ужин'}
        colours = {'Breakfast': 'orange', 'Lunch': 'green', 'Dinner': 'purple'}
        for tag, value in tags.items():
            Tag.objects.create(pk=pk, name=Tag.Status(value), colour=colours.get(tag), slug=tag.lower())
            pk += 1
