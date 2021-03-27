from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from cookbook.models import RecipePost


def add_recipe(user_id, form, cd):
    slug = slugify(cd['title'])
    new_recipe = form.save(commit=False)
    new_recipe.author_id = user_id
    new_recipe.slug = slug
    new_recipe.save()


# Tested
def get_recipe(author, recipe_id):
    try:
        result = RecipePost.objects.get(id=recipe_id, author=author)
    except RecipePost.DoesNotExist:
        result = False
    return result


def get_recipe_with_date(year, month, day, slug):
    return get_object_or_404(RecipePost, slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)


# Tested
def get_recipe_with_title(title: str):
    recipe = RecipePost.objects.all().filter(title=title)
    return recipe if recipe else False


def get_user_recipes(author):
    return RecipePost.objects.all().filter(author=author)


def get_recipe_with_id(id):
    return get_object_or_404(RecipePost, id=id)


def save_recipe(recipe):
    recipe.save()


def delete_recipe(recipe_pk):
    recipe = RecipePost.objects.get(id=recipe_pk)
    recipe.delete()
