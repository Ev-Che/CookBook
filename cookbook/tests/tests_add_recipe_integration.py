from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cookbook.models import RecipePost


class AddRecipeTests(TestCase):
    def setUp(self):
        self.recipe_data = {'title': 'title',
                            'author': self.client,
                            'body': 'body'}

    def test_add_recipe_post__user_is_not_auth__redirect_to_login_page_and_do_not_add_recipe_to_DB(self):
        expected_reverse_url = reverse('account:login')
        expected_count_of_recipes_in_db = 0

        response = self.client.post(reverse('cookbook:add_recipe'),
                                    data=self.recipe_data, follow=True)
        actual_count_of_recipes_in_db = len(RecipePost.objects.all())

        self.assertRedirects(response, expected_reverse_url)
        self.assertEqual(expected_count_of_recipes_in_db, actual_count_of_recipes_in_db)

    def test_add_recipe_post__invalid_form__show_add_recipe_page_with_errors_and_do_not_add_recipe_to_DB(self, ):
        expected_template = 'cookbook/adding_recipe/add_recipe.html'
        user = User.objects.create(username='Ev-Che')
        user.set_password('ev123456')
        user.save()
        self.client.login(username='Ev-Che', password='ev123456')
        self.recipe_data['title'] = ''
        expected_count_of_recipes_in_db = 0

        response = self.client.post(reverse('cookbook:add_recipe'),
                                    data=self.recipe_data, follow=True)
        actual_count_of_recipes_in_db = len(RecipePost.objects.all())

        self.assertTemplateUsed(response, expected_template)
        self.assertEqual(expected_count_of_recipes_in_db, actual_count_of_recipes_in_db)

    def test_add_recipe_post__form_is_valid_show_successfully_added_page_and_add_recipe_to_db(self):
        expected_page_template = 'cookbook/adding_recipe/successfully_added.html'
        user = User.objects.create(username='Ev-Che')
        user.set_password('ev123456')
        user.save()
        self.client.login(username='Ev-Che', password='ev123456')
        expected_count_of_recipes_in_db = 1

        response = self.client.post(reverse('cookbook:add_recipe'), data=self.recipe_data)
        actual_count_of_recipes_in_db = len(RecipePost.objects.all())

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(expected_count_of_recipes_in_db, actual_count_of_recipes_in_db)
