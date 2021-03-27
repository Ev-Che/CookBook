from django.contrib.auth.models import User
from django.test import TestCase

from django.urls import reverse


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.data = {'username': '',
                     'first_name': 'first_name',
                     'password': '12345',
                     'password2': '12345'}

    def test_user_registration_post__enter_invalid_data__show_error_page_do_not_add_user_to_DB(self):
        expected_page_template = 'account/register.html'
        expected_count_of_users_in_db = 0

        response = self.client.post(reverse('account:register'), data=self.data)
        actual_count_of_users_in_db = len(User.objects.all())

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(expected_count_of_users_in_db, actual_count_of_users_in_db)

    def test_user_registration_post__enter_valid_data__show_registration_done_page_and_add_user_to_DB(self):
        expected_page_template = 'account/register_done.html'
        self.data['username'] = 'username'
        expected_count_of_users_in_db = 1

        response = self.client.post(reverse('account:register'), data=self.data)
        actual_count_of_users_in_db = len(User.objects.all())

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(expected_count_of_users_in_db, actual_count_of_users_in_db)
