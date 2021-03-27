from django_webtest import WebTest

from django.urls import reverse

from django.contrib.auth.models import User


class GetUserRecipesTests(WebTest):

    def test_get_user_recipes__client_not_authorized__redirect_to_login_page(self):
        expected_redirect_url = '/account/login/?next=/cookbook/user_cookbook/'
        expected_page_template = 'account/login.html'

        response = self.client.get(reverse('cookbook:user_cookbook'), follow=True)

        self.assertTemplateUsed(response, expected_page_template)
        self.assertRedirects(response, expected_redirect_url)

    def test_get_user_recipes__client_authorized__get_user_recipes_page(self):
        expected_page_template = 'cookbook/user_cookbook.html'
        user = User.objects.create(username='Ev-Che')
        user.set_password('ev123456')
        user.save()

        is_login = self.client.login(username='Ev-Che', password='ev123456')
        response = self.client.get(reverse('cookbook:user_cookbook'))

        self.assertTrue(is_login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, expected_page_template)
