from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserLoginViewTests(TestCase):

    def test_user_login_get__user_is_not_auth__show_login_page(self):
        expected_page_template = 'account/login.html'

        response = self.client.get(reverse('account:login'))

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(response.status_code, 200)

    def test_user_login_get__user_is_auth__redirect_to_user_cookbook(self):
        expected_redirect_url = '/cookbook/user_cookbook/'
        expected_page_template = 'cookbook/user_cookbook.html'
        user = User.objects.create(username='Ev-Che')
        user.set_password('ev123456')
        user.save()

        is_login = self.client.login(username='Ev-Che', password='ev123456')
        response = self.client.get(reverse('account:login'), follow=True)

        self.assertTrue(is_login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, expected_page_template)
        self.assertRedirects(response, expected_redirect_url)

    def test_user_login_post__form_is_not_valid__show_login_page_with_errors(self):
        expected_page_template = 'account/login.html'
        data = {'username': '', 'password': ''}

        response = self.client.post(reverse('account:login'), data=data, follow=True)

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(response.status_code, 200)

    def test_user_login_post__no_such_user_in_DB__show_login_page_with_errors(self):
        expected_page_template = 'account/login.html'
        data = {'username': 'user123', 'password': '54321'}

        response = self.client.post(reverse('account:login'), data=data, follow=True)

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid login or password.')

    def test_user_login_post__user_exists___user_is_auth_and_show_user_cookbook(self):
        expected_page_template = 'cookbook/user_cookbook.html'
        data = {'username': 'Ev-Che', 'password': 'ev123456'}
        user = User.objects.create(username='Ev-Che')
        user.set_password('ev123456')
        user.save()

        response = self.client.post(reverse('account:login'), data=data, follow=True)

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.is_authenticated, True)
