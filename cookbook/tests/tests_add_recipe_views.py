from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from mock import patch


class AddRecipeTests(TestCase):
    def setUp(self):
        self.recipe_data = {'title': 'title',
                            'author': self.client,
                            'body': 'body'}

    @patch('cookbook.views.services.add_recipe')
    def test_add_recipe_post__user_is_not_auth__redirect_to_login_page(self, mock_obj):
        expected_reverse_url = reverse('account:login')

        response = self.client.post(reverse('cookbook:add_recipe'),
                                    data=self.recipe_data, follow=True)

        self.assertRedirects(response, expected_reverse_url)
        self.assertEqual(response.status_code, 200)

    @patch('cookbook.views.services.add_recipe')
    def test_add_recipe_post__invalid_form__show_add_recipe_page_with_errors(self, mock_obj):
        expected_template = 'cookbook/adding_recipe/add_recipe.html'
        user = User.objects.create(username='Ev-Che')
        user.set_password('ev123456')
        user.save()
        self.client.login(username='Ev-Che', password='ev123456')
        self.recipe_data['title'] = ''

        response = self.client.post(reverse('cookbook:add_recipe'),
                                    data=self.recipe_data, follow=True)

        self.assertTemplateUsed(response, expected_template)
        self.assertEqual(response.status_code, 200)

    @patch('cookbook.views.services.add_recipe')
    def test_add_recipe_post__form_is_valid_show_successfully_added_page(self, mock):
        expected_page_template = 'cookbook/adding_recipe/successfully_added.html'
        user = User.objects.create(username='Ev-Che')
        user.set_password('ev123456')
        user.save()
        self.client.login(username='Ev-Che', password='ev123456')

        response = self.client.post(reverse('cookbook:add_recipe'), data=self.recipe_data)

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(response.status_code, 200)
