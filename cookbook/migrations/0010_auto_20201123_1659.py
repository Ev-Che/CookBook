# Generated by Django 3.1.2 on 2020-11-23 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0009_remove_recipepost_users_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipepost',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
