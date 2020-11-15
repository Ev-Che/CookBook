from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory, Client
from .models import RecipePost
from .views import recipe_detail, delete_recipe, get_user_recipes
import tempfile
from django.http import Http404


class RecipeDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username')
        self.request = RequestFactory()

    def test_recipe_detail__recipe_exist__successful_receipt_recipe_page(self):
        photo = tempfile.NamedTemporaryFile(suffix='.jpg').name
        recipe = RecipePost.objects.create(title='title',
                                           slug='title',
                                           author=self.user,
                                           body='body',
                                           photo=photo)
        path = 'http://127.0.0.1:8000/cookbook/' + str(recipe.publish.year) + '/' + \
               str(recipe.publish.month) + '/' + str(recipe.publish.day) + '/' + \
               str(recipe.slug)
        get_request = self.request.get(path=path)

        response = recipe_detail(get_request, recipe.publish.year,
                                 recipe.publish.month,
                                 recipe.publish.day,
                                 recipe.slug)

        self.assertContains(response, recipe.title, html=True)

    def test_recipe_detail__recipe_does_not_exist__raise_404(self):
        path = 'http://127.0.0.1:8000/cookbook/2020/10/10/slug'
        get_request = self.request.get(path=path)
        with self.assertRaises(Http404):
            recipe_detail(get_request, '2020', '10', '10', 'slug')


class DeleteRecipeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='username')
        self.request = RequestFactory()
        photo = tempfile.NamedTemporaryFile(suffix='.jpg').name
        self.recipe = RecipePost.objects.create(title='title',
                                                slug='title',
                                                author=self.user,
                                                body='body',
                                                photo=photo)
        self.path = 'http://127.0.0.1:8000/cookbook/' + str(self.recipe.id) + '/deletion'

    def test_delete_recipe__recipe_exists_and_user_is_author__delete_from_DB(self):
        post_request = self.request.post(self.path)
        post_request.user = self.user
        # with patch("cookbook.views.delete_recipe.messages") as mock_messages:
        #     mock_messages.add_message = MagicMock()
        response = delete_recipe(post_request, self.recipe.id)
        expected = 0
        self.assertEqual(len(RecipePost.objects.all()), expected)

    def test_delete_recipe__recipe_exists_and_user_is_not_author__do_not_delete_from_DB(self):
        post_request = self.request.post(self.path)
        user2 = User.objects.create(username='user2')
        post_request.user = user2

        response = delete_recipe(post_request, self.recipe.id)
        expected = 1
        self.assertEqual(len(RecipePost.objects.all()), expected)


class GetUserRecipesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username')
        self.request = RequestFactory()
        self.path = 'http://127.0.0.1:8000/cookbook/user_cookbook/'

    def test_get_user_recipes__user_added_one_recipe__exist_one_recipe(self):
        photo = tempfile.NamedTemporaryFile(suffix='.jpg').name
        recipe = RecipePost.objects.create(title='title',
                                           slug='title',
                                           author=self.user,
                                           body='body',
                                           photo=photo)

        get_request = self.request.get(self.path)
        get_request.user = self.user

        user_recipes = get_user_recipes(get_request)
        expected = 1
        self.assertEqual(len(user_recipes), expected)

    def test_get_user_recipes__user_did_not_add_recipe__no_existed_recipes(self):
        get_request = self.request.get(self.path)
        get_request.user = self.user
        user_recipes = get_user_recipes(get_request)
        expected = 0
        self.assertEqual(len(user_recipes), expected)
