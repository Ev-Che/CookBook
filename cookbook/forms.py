from django import forms
from .models import RecipePost


class SearchForm(forms.Form):
    query = forms.CharField()


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = RecipePost
        fields = ['title', 'body', 'photo']
        exclude = ['author']


class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = RecipePost
        fields = ['title', 'body']
