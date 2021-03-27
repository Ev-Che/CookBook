from django.urls import path, include
from . import views


app_name = 'cookbook'

urlpatterns = [
    path('', views.RecipeListView.as_view(),  name='recipe_list'),
    path('user_cookbook/', views.user_cookbook, name='user_cookbook'),
    path('<int:year>/<int:month>/<int:day>/<slug:recipe>/',
         views.recipe_detail, name='recipe_detail'),
    path('search/', views.recipe_search_view, name='recipe_search'),
    path('add/', views.AddRecipe.as_view(), name='add_recipe'),
    path('<int:recipe_id>/editing/',
         views.EditRecipe.as_view(), name='edit_recipe'),
    path('<int:recipe_id>/deletion/', views.delete_recipe, name='delete_recipe'),
    path('assessment/', include('likes.urls', namespace='likes'))
]
