from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
