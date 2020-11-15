from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase
from .views import UserRegister
from django.test.client import RequestFactory


class UserRegistrationFormTests(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.path = 'http://127.0.0.1:8000/account/register/'
        self.data = {'username': 'username',
                     'first_name': 'first_name',
                     'password': 'use123456',
                     'password2': 'use123456'}
        self.user_register = UserRegister()

    def test_post__check_first_name_has_forbidden_character__raise_exception_message(self):
        # Arrange
        self.data['first_name'] = 'Av='
        post_request = self.request.post(self.path, self.data)
        expected_message = 'Field First Name must contain only Latin' \
                           ' characters, numbers and underscore.'
        # Act
        response = self.user_register.post(post_request)
        # Assert
        self.assertContains(response, expected_message, html=True)

    def test_post__check_first_name_is_not_long_enough__raise_exception_message(self):
        # Arrange
        self.data['first_name'] = 'Av'
        post_request = self.request.post(self.path, data=self.data)
        expected_message = 'The First name field must be at least 3 characters long.'
        # Act
        response = self.user_register.post(post_request)
        # Assert
        self.assertContains(response, expected_message, html=True)

    def test_post__first_name_meets_all_restrictions__added_to_DB(self):
        # Arrange
        self.data['first_name'] = 'Alex'
        post_request = self.request.post(self.path, data=self.data)
        # Act
        self.user_register.post(post_request)
        # Assert
        expected = 1
        self.assertEqual(len(User.objects.all()), expected)

    def test_post__equal_passwords__added_user_to_DB(self):
        # Arrange
        post_request = self.request.post(self.path, data=self.data)
        expected = 1
        # Act
        self.user_register.post(post_request)
        # Assert
        self.assertEqual(len(User.objects.all()), expected)

    def test_post__unequal_passwords__raise_exception(self):
        # Arrange
        self.data['password2'] = '123456'
        post_request = self.request.post(self.path, self.data)
        expected_message = 'Passwords don\'t match.'
        # Act
        response = self.user_register.post(post_request)
        # Assert
        self.assertContains(response, expected_message, html=True)
