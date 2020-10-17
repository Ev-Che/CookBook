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
