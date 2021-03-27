from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cookbook.models import RecipePost


class EditRecipeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Ev-Che')
        self.user.set_password('ev123456')
        self.user.save()
        self.recipe = RecipePost.objects.create(title='title',
                                                slug='title',
                                                author=self.user,
                                                body='body')
        self.recipe_data = {'title': 'new_title', 'body': 'body'}

    def test_edit_recipe_post__form_is_valid__show_success_page(self):
        expected_page_template = 'cookbook/editing_recipe/done_editing.html'
        expected_title = self.recipe_data['title']
        self.client.login(username='Ev-Che', password='ev123456')

        response = self.client.post(reverse('cookbook:edit_recipe', args=[self.recipe.id]),
                                    data=self.recipe_data)
        actual_recipe_title = RecipePost.objects.get(author=self.user).title

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(actual_recipe_title, expected_title)

    def test_edit_recipe_post__client_is_not_auth__redirect_to_login_page(self):
        expected_reverse_url = reverse('account:login')
        expected_title = self.recipe.title

        response = self.client.post(reverse('cookbook:edit_recipe', args=[self.recipe.id]),
                                    data=self.recipe_data, follow=True)
        actual_recipe_title = RecipePost.objects.get(author=self.user).title

        self.assertRedirects(response, expected_reverse_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(actual_recipe_title, expected_title)

    def test_edit_recipe_post__invalid_form__show_add_recipe_page_with_errors(self):
        expected_template = 'cookbook/editing_recipe/edit.html'
        self.client.login(username='Ev-Che', password='ev123456')
        self.recipe_data['title'] = ''
        expected_title = self.recipe.title

        response = self.client.post(reverse('cookbook:edit_recipe', args=[self.recipe.id]),
                                    data=self.recipe_data, follow=True)
        actual_recipe_title = RecipePost.objects.get(author=self.user).title

        self.assertTemplateUsed(response, expected_template)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(actual_recipe_title, expected_title)
