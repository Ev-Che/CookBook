from django.shortcuts import redirect, get_object_or_404
from .services import *
from cookbook.models import RecipePost


def like_the_recipe(request, recipe_id):
    recipe = get_object_or_404(RecipePost, pk=recipe_id)
    add_like(recipe, request.user)
    print(f'{request.user.first_name} liked post. Total likes: {recipe.total_likes}')
    return redirect('cookbook:recipe_detail', year=recipe.publish.year,
                    month=recipe.publish.month,
                    day=recipe.publish.day,
                    recipe=recipe.slug)


def dislike_the_recipe(request, recipe_id):
    recipe = get_object_or_404(RecipePost, pk=recipe_id)
    remove_like(recipe, request.user)
    print(f'{request.user.first_name} disliked post. Total likes: {recipe.total_likes}')
    return redirect('cookbook:recipe_detail', year=recipe.publish.year,
                    month=recipe.publish.month,
                    day=recipe.publish.day,
                    recipe=recipe.slug)
