from django.contrib import admin
from .models import RecipePost


@admin.register(RecipePost)
class RecipePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish')
    list_filter = ('publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}  # auto fill slug field
    # raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('publish',)
