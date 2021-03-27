from django.test import TestCase

from cookbook.services import add_recipe
from cookbook.models import RecipePost
from cookbook.forms import AddRecipeForm

from django.contrib.auth.models import User


class AddRecipeServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username')
        self.recipe_data = {'title': 'title',
                            'author': self.client,
                            'body': 'body'}

    def test_add_recipe__add_recipe_to_db__count_of_recipes_increased(self):
        form = AddRecipeForm(data=self.recipe_data)
        expected_count = len(RecipePost.objects.all()) + 1

        add_recipe(self.user.id, form, form.data)
        actual_count = len(RecipePost.objects.all())

        self.assertEqual(actual_count, expected_count)
