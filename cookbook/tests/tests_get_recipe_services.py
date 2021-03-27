from django.test import TestCase

from cookbook.services import get_recipe
from cookbook.models import RecipePost

from django.contrib.auth.models import User


class GetRecipeServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username')
        self.recipe = RecipePost.objects.create(title='title',
                                                slug='slug',
                                                author=self.user,
                                                body='body')

    def test_get_recipe__not_found_id__False(self):
        expected = False

        actual = get_recipe(self.user, 1000)

        self.assertEqual(actual, expected)

    def test_get_recipe__not_found_author__False(self):
        wrong_user = User.objects.create(username='wrong_user')
        expected = False

        actual = get_recipe(wrong_user, self.recipe.id)

        self.assertEqual(expected, actual)

    def test_get_recipe__recipe_exist__recipe(self):
        expected = RecipePost.objects.all()
        expected_len = 1

        actual = get_recipe(self.user, self.recipe.id)

        self.assertEqual(actual, self.recipe)
