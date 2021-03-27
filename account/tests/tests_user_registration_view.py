from django.test import TestCase
from mock import patch

from django.urls import reverse


class UserRegistrationViewTests(TestCase):
    def setUp(self):
        self.data = {'username': '',
                     'first_name': 'first_name',
                     'password': '12345',
                     'password2': '12345'}

    @patch('account.views.user_register', return_value='mock obj')
    def test_user_registration_post__enter_invalid_data__show_registration_page_with_errors(self, mock_obj):
        expected_page_template = 'account/register.html'

        response = self.client.post(reverse('account:register'), data=self.data)

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(response.status_code, 200)

    @patch('account.views.user_register', return_value='mock obj')
    def test_user_registration_post__enter_valid_data__show_registration_done_page(self, mock_obj):
        expected_page_template = 'account/register_done.html'
        self.data['username'] = 'username'

        response = self.client.post(reverse('account:register'), data=self.data)

        self.assertTemplateUsed(response, expected_page_template)
        self.assertEqual(response.status_code, 200)
