# Generated by Django 3.0.8 on 2021-04-19 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20210419_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Время приготовления'),
        ),
    ]
