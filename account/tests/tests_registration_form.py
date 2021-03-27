from django.test import TestCase

from parameterized import parameterized

from account.forms import UserRegistrationForm


class CleanPasswordTests(TestCase):
    def setUp(self):
        self.data = {'username': 'username',
                     'first_name': 'first_name'}

    @parameterized.expand([
        ['12345', '54321', 'Passwords don\'t match.'],
        ['123', '123', 'The password must be at least 5 characters long.'],
        ['012345678901234567890', '012345678901234567890',
         'The password field must be shortest that 20 characters long.']
    ])
    def test_clean_password2__not_correct_passwords__False(self, password, password2, expected_message):
        self.data['password'] = password
        self.data['password2'] = password2
        expected_response = False

        form = UserRegistrationForm(data=self.data)
        actual_response = form.is_valid()
        actual_message = form.errors.get_json_data(escape_html=False)['password'][0]['message']

        self.assertEqual(actual_response, expected_response)
        self.assertEqual(actual_message, expected_message)

    @parameterized.expand([
        ['strongpassword123'],
        ['12345'],
        ['verystrongpassword1']
    ])
    def test_clean_password2__correct_passwords__True(self, password):
        self.data['password'] = self.data['password2'] = password
        expected = True

        form = UserRegistrationForm(data=self.data)

        self.assertEqual(form.is_valid(), expected)


class CleanUserNameTests(TestCase):
    def setUp(self):
        self.data = {'username': 'username',
                     'first_name': 'first_name',
                     'password': '12345',
                     'password2': '12345'}

    @parameterized.expand([
        ['ab', 'The Username field must be at least 3 characters long.'],
        ['a', 'The Username field must be at least 3 characters long.'],
        ['123451234512345123451', 'The Username field must be shortest that 20'
                                  ' characters long.']
    ])
    def test_clean_username__not_correct_username__False(self, username, expected_message):
        self.data['username'] = username
        expected_response = False

        form = UserRegistrationForm(data=self.data)
        actual_response = form.is_valid()
        actual_message = form.errors.get_json_data(escape_html=False)['username'][0]['message']

        self.assertEqual(actual_response, expected_response)
        self.assertEqual(actual_message, expected_message)

    @parameterized.expand([
        'Jan',
        'JohnJohnJohnJohnJoh',
        'Vladimir'
    ])
    def test_clean_username__correct_username__True(self, username):
        expected_response = True
        self.data['username'] = username

        form = UserRegistrationForm(data=self.data)
        actual_response = form.is_valid()

        self.assertEqual(actual_response, expected_response)


class CleanFirstNameTests(TestCase):
    def setUp(self):
        self.data = {'username': 'username',
                     'password': '12345',
                     'password2': '12345'}

    @parameterized.expand([
        ['ab', 'The First name field must be at least 3 '
               'characters long.'],
        ['ab', 'The First name field must be at least 3 '
               'characters long.'],
        ['12345123451234512345', 'The First name field must be shortest that 20'
                                 ' characters long.'],
        ['ab#', 'Field First Name must '
                'contain only Latin characters, '
                'numbers and underscore.'],
        ['***', 'Field First Name must '
                'contain only Latin characters, '
                'numbers and underscore.'],
        ['&&&', 'Field First Name must '
                'contain only Latin characters, '
                'numbers and underscore.']
    ])
    def test_clean_first_name__not_correct_first_name__False(self, first_name, expected_message):
        self.data['first_name'] = first_name
        expected = False

        form = UserRegistrationForm(data=self.data)
        actual_result = form.is_valid()
        actual_message = form.errors.get_json_data(escape_html=False)['first_name'][0]['message']
        self.assertEqual(actual_result, expected)
        self.assertEqual(actual_message, expected_message)

    @parameterized.expand([
        ['Alex'],
        ['AlexAlexAlexAlexAle'],
        ['Pavel'],
        ['Jan']
    ])
    def test_clean_first_name__correct_first_name__True(self, first_name):
        self.data['first_name'] = first_name
        expected = True

        form = UserRegistrationForm(data=self.data)
        result = form.is_valid()

        self.assertEqual(result, expected)
