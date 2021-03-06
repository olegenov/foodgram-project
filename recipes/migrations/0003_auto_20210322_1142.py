# Generated by Django 3.0.8 on 2021-03-22 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20210322_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingradient',
            name='units',
            field=models.CharField(max_length=200, verbose_name='Единицы измерения'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
