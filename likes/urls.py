from django.urls import path
from . import views


app_name = 'likes'

urlpatterns = [
    path('<int:recipe_id>/like/', views.like_the_recipe, name='like_recipe'),
    path('<int:recipe_id>/dislike/', views.dislike_the_recipe, name='dislike_recipe'),
]
