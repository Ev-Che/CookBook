from django.shortcuts import render, get_object_or_404, redirect

from .models import RecipePost
from django.views.generic import ListView
from .forms import SearchForm, AddRecipeForm, EditRecipeForm
from django.views.generic import View

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from likes import services as likes_services
from . import services


class RecipeListView(ListView):
    queryset = RecipePost.objects.all()
    context_object_name = 'recipes'
    paginate_by = 3
    template_name = 'cookbook/cookbook_list.html'


# tested
def recipe_detail(request, year, month, day, recipe):
    recipe = services.get_recipe_with_date(year, month, day, recipe)
    print(recipe.pk)
    is_fan = likes_services.is_fan(recipe, request.user)
    print(is_fan)
    likes = recipe.total_likes
    print(f'{likes}')
    return render(request, 'cookbook/recipe_detail.html',
                  {'recipe': recipe, 'is_fan': is_fan,
                   'total_likes': likes})


# tested (create TDD!!!)
def recipe_search_view(request):
    form = SearchForm()
    results = []
    query = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = services.get_recipe_with_title(query)
            print(results)
    return render(request, 'cookbook/search.html',
                  {'form': form, 'query': query,
                   'results': results, 'section': 'search'})


# tested
class AddRecipe(View):
    form_class = AddRecipeForm
    template_name = ['cookbook/adding_recipe/add_recipe.html',
                     'cookbook/adding_recipe/successfully_added.html']

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('account:login')
        form = self.form_class()
        return render(request, self.template_name[0],
                      {'form': form, 'section': 'user_add_recipe'})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('account:login')

        form = self.form_class(request.POST, request.FILES)
        template = self.template_name[0]
        context = {'form': form, 'section': 'user_add_recipe'}
        if form.is_valid():
            services.add_recipe(request.user.id, form, form.cleaned_data)
            template = self.template_name[1]
            context = {}
        print(form.errors)

        return render(request, template, context)


@login_required
def user_cookbook(request):
    user_recipes = services.get_user_recipes(request.user)
    return render(request,
                  'cookbook/user_cookbook.html',
                  {'section': 'user_cookbook',
                   'user_recipes': user_recipes})


class EditRecipe(View):
    form_class = EditRecipeForm
    template_name = ['cookbook/editing_recipe/edit.html',
                     'cookbook/editing_recipe/done_editing.html']

    def get(self, request, recipe_id):
        recipe = services.get_recipe_with_id(recipe_id)
        form = self.form_class(initial={'title': recipe.title,
                                        'body': recipe.body})
        return render(request, self.template_name[0],
                      {'form': form})

    def post(self, request, recipe_id):
        if not request.user.is_authenticated:
            return redirect('account:login')
        recipe = services.get_recipe(request.user, recipe_id)
        form = self.form_class(request.POST, instance=recipe)
        template = self.template_name[0]
        context = {'form': form}
        if form.is_valid():
            services.save_recipe(recipe)
            template = self.template_name[1]
            context = {}
        return render(request, template, context)


# tested
def delete_recipe(request, recipe_id):
    template = 'cookbook/fail_deleting.html'
    if not request.user.is_authenticated:
        return redirect('account:login')
    recipe = services.get_recipe(request.user, recipe_id)
    if recipe:
        services.delete_recipe(recipe.id)
        template = 'cookbook/success_deleted.html'
    return render(request, template)


def find_recipe_with_id_and_user(recipe_id, author):
    return RecipePost.objects.all().filter(pk=recipe_id,
                                           author=author)
