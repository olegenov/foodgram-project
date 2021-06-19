from django.forms import ModelForm, Textarea

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'image', 'time']
        widgets = {
            'description': Textarea(attrs={'cols': 50, 'rows': 10})
        }
