from django.contrib.auth.models import User
from django.test import TestCase

from django.urls import reverse
from mock import patch


class DeleteRecipeViewTests(TestCase):

    def test_delete_recipe_post__user_is_not_auth__redirect_to_login_page(self):
        expected_reverse_url = reverse('account:login')

        response = self.client.post(reverse('cookbook:delete_recipe', args=[1]), follow=True)

        self.assertRedirects(response, expected_reverse_url)
        self.assertEqual(response.status_code, 200)

    @patch('cookbook.views.services.get_recipe')
    @patch('cookbook.views.services.delete_recipe')
    def test_delete_recipe_post__recipe_exists__show_successfully_deleted_page(self, mock_recipe, mock_deleting):
        expected_page_template = 'cookbook/success_deleted.html'
        user = User.objects.create(username='Ev-Che')
        user.set_password('ev123456')
        user.save()
        self.client.login(username='Ev-Che', password='ev123456')

        response = self.client.post(reverse('cookbook:delete_recipe', args=[1]), follow=True)

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(response.status_code, 200)

    @patch('cookbook.views.services.get_recipe', return_value=False)
    def test_delete_recipe_post__recipe_does_not_exists__show_error_page(self, mock_recipe):
        expected_page_template = 'cookbook/fail_deleting.html'
        user = User.objects.create(username='Ev-Che')
        user.set_password('ev123456')
        user.save()
        self.client.login(username='Ev-Che', password='ev123456')

        response = self.client.post(reverse('cookbook:delete_recipe', args=[1]), follow=True)

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(response.status_code, 200)
