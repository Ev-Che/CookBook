from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from likes.models import Like


class RecipePost(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50,
                            unique_for_date='publish',
                            blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe_posts')  # Many to one
    body = models.TextField(unique=True)
    publish = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    likes = GenericRelation(Like)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cookbook:recipe_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    @property
    def total_likes(self):
        return self.likes.count()
