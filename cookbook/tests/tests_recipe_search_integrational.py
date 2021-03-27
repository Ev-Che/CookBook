from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from cookbook.models import RecipePost


class RecipeSearchViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='username')
        self.recipe = RecipePost.objects.create(title='title',
                                                slug='title',
                                                author=self.user,
                                                body='body')
        self.client = Client()
        self.path = reverse('cookbook:recipe_search')
        self.data = {'query': self.recipe.title}

    def test_recipe_search__recipe_with_given_title_existed__exist_one_recipe(self):
        expected = 1
        expected_template = 'cookbook/search.html'

        response = self.client.get(self.path, data=self.data)

        self.assertEqual(len(response.context['results']), expected)

    def test_recipe_search__recipe_with_given_title_not_existed__False(self):
        expected = False
        self.data['query'] = 'not_existed_recipe'

        response = self.client.get(self.path, data=self.data)

        self.assertEqual(response.context['results'], expected)
