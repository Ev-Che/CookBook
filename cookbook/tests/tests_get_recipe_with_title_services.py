from django.test import TestCase

from cookbook.services import get_recipe_with_title
from cookbook.models import RecipePost

from django.contrib.auth.models import User


class RecipeSearchServiceTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='username')
        self.recipe = RecipePost.objects.create(title='title',
                                                slug='slug',
                                                author=user,
                                                body='body')

    def test_recipe_search__not_found__false(self):
        expected = False

        actual = get_recipe_with_title('')

        self.assertEqual(actual, expected)

    def test_recipe_search__recipe_exist__get_recipe(self):
        expected = RecipePost.objects.all()
        expected_len = 1

        actual = get_recipe_with_title('title')

        self.assertEqual(len(actual), expected_len)
        self.assertQuerysetEqual(actual, expected, transform=lambda x: x)
