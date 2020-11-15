import re

from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput,
                               min_length=3, max_length=20)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput,
                                min_length=3, max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            self.add_error('username', 'The Username field must be at least 3'
                                       'characters long.')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 3:
            self.add_error('first_name', 'The First name field must be at least 3 '
                                         'characters long.')
        elif not re.match(r'[a-zA-Z_]+$', first_name):
            self.add_error('first_name', 'Field First Name must '
                                         'contain only Latin characters, '
                                         'numbers and underscore.')
        return first_name
