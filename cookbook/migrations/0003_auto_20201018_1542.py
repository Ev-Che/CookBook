# Generated by Django 3.1.2 on 2020-10-18 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0002_auto_20201018_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipepost',
            name='photo',
            field=models.ImageField(height_field=100, upload_to='recipe_photos', width_field=100),
        ),
    ]
