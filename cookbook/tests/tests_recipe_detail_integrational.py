from django.test import TestCase
from django.test.client import RequestFactory

from django.contrib.auth.models import User

from django.http import Http404
from django.urls import reverse

from ..models import RecipePost
from ..views import recipe_detail


class RecipeDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username')
        self.request = RequestFactory()

    def test_recipe_detail__recipe_exist__successful_receipt_recipe_page(self):
        recipe = RecipePost.objects.create(title='title',
                                           slug='title',
                                           author=self.user,
                                           body='body')
        path = reverse('cookbook:recipe_detail', args=(recipe.publish.year,
                                                       recipe.publish.month,
                                                       recipe.publish.day,
                                                       recipe.slug))
        get_request = self.request.get(path=path)
        get_request.user = self.user

        response = recipe_detail(get_request, recipe.publish.year,
                                 recipe.publish.month,
                                 recipe.publish.day,
                                 recipe.slug)

        self.assertContains(response, recipe.title, html=True)

    def test_recipe_detail__recipe_does_not_exist__raise_404(self):
        path = reverse('cookbook:recipe_detail', args=(2020, 10, 10, 'slug'))
        get_request = self.request.get(path=path)
        with self.assertRaises(Http404):
            recipe_detail(get_request, '2020', '10', '10', 'slug')
