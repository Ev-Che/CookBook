from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from cookbook.models import RecipePost
from cookbook.views import delete_recipe


class DeleteRecipeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username')
        self.request = RequestFactory()
        self.recipe = RecipePost.objects.create(title='title',
                                                slug='title',
                                                author=self.user,
                                                body='body')
        self.path = 'http://127.0.0.1:8000/cookbook/' + str(self.recipe.id) + '/deletion'

    def test_delete_recipe__recipe_exists_and_user_is_author__delete_from_DB(self):
        post_request = self.request.post(self.path)
        post_request.user = self.user

        response = delete_recipe(post_request, self.recipe.id)
        expected = 0

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(RecipePost.objects.all()), expected)

    def test_delete_recipe__recipe_exists_and_user_is_not_author__do_not_delete_from_DB(self):
        post_request = self.request.post(self.path)
        user2 = User.objects.create(username='user2')
        post_request.user = user2

        response = delete_recipe(post_request, self.recipe.id)
        expected = 1

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(RecipePost.objects.all()), expected)

    def test_delete_recipe__user_is_not_auth__redirect_to_login_page(self):
        expected_redirect_url = reverse('account:login')

        response = self.client.post(reverse('cookbook:delete_recipe', args=[self.recipe.id]), follow=True)
        expected = 1

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, expected_redirect_url)
        self.assertEqual(len(RecipePost.objects.all()), expected)
