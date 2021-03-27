from django.test import TestCase
from mock import Mock

from likes.services import *
from cookbook.models import RecipePost


class LikeServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username')
        self.recipe = RecipePost.objects.create(title='title',
                                                slug='slug',
                                                author=self.user,
                                                body='body')

    def test_add_like__add_like_to_recipe__count_of_likes_is_1(self):
        expected_count = self.recipe.total_likes + 1
        expected_result = True

        actual = add_like(self.recipe, self.user)

        self.assertEqual(actual, expected_result)
        self.assertEqual(self.recipe.total_likes, expected_count)

    def test_remove_like__remove_like_from_recipe__count_of_likes_was_1_now_0(self):
        add_like(self.recipe, self.user)
        expected_response = True
        expected_count = self.recipe.total_likes - 1

        actual_response = remove_like(self.recipe, self.user)
        actual_count = self.recipe.total_likes

        self.assertEqual(actual_count, expected_count)
        self.assertEqual(actual_response, expected_response)

    def test_is_fan__user_like_recipe__True(self):
        mock_user = Mock()
        mock_user.is_authenticated = Mock(return_value=True)
        expected = True
        add_like(self.recipe, self.user)

        actual = is_fan(self.recipe, self.user)

        self.assertEqual(expected, actual)

    def test_is_fan__user_do_not_like_recipe__False(self):
        expected = False

        actual = is_fan(self.recipe, self.user)

        self.assertEqual(expected, actual)

    def test_is_fan__user_do_not_auth__False(self):
        expected = False
        mock_user = Mock()
        mock_user.is_authenticated = False

        actual = is_fan(self.recipe, mock_user)

        self.assertEqual(expected, actual)
