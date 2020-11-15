from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify

from .models import RecipePost
from django.views.generic import ListView
from .forms import SearchForm, AddRecipeForm, EditRecipeForm
from django.views.generic import View

from django.contrib.auth.decorators import login_required

from django.contrib import messages


class RecipeListView(ListView):
    queryset = RecipePost.objects.all()
    context_object_name = 'recipes'
    paginate_by = 3
    template_name = 'cookbook/cookbook_list.html'


def recipe_detail(request, year, month, day, recipe):
    recipe = get_object_or_404(RecipePost, slug=recipe,
                               publish__year=year,
                               publish__month=month,
                               publish__day=day)
    print(recipe.pk)
    return render(request, 'cookbook/recipe_detail.html',
                  {'recipe': recipe})


def recipe_search(request):
    form = SearchForm()
    results = []
    query = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = RecipePost.objects.all().filter(title=query)
    return render(request, 'cookbook/search.html',
                  {'form': form, 'query': query,
                   'results': results, 'section': 'search'})


class AddRecipe(View):
    form_class = AddRecipeForm
    template_name = ['cookbook/adding_recipe/add_recipe.html',
                     'cookbook/adding_recipe/successfully_added.html']

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name[0],
                      {'form': form, 'section': 'user_add_recipe'})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            slug = slugify(cd['title'])
            new_recipe = form.save(commit=False)
            new_recipe.author_id = request.user.id
            new_recipe.slug = slug
            new_recipe.save()
            print(request.user.id)
            return render(request, self.template_name[1],
                          {'cd': cd})
        print(form.errors)
        return render(request, self.template_name[0],
                      {'form': form, 'section': 'user_add_recipe'})


@login_required
def user_cookbook(request):
    user_recipes = RecipePost.objects.all().filter(author=request.user)
    return render(request,
                  'cookbook/user_cookbook.html',
                  {'section': 'user_cookbook',
                   'user_recipes': user_recipes})


# def get_user_recipes(request):
#     return RecipePost.objects.all().filter(author=request.user)


class EditRecipe(View):
    form_class = EditRecipeForm
    template_name = ['cookbook/editing_recipe/edit.html',
                     'cookbook/editing_recipe/done_editing.html']

    def get(self, request, recipe_id):
        recipe = get_object_or_404(RecipePost, id=recipe_id)
        form = self.form_class(initial={'title': recipe.title,
                                        'body': recipe.body})
        return render(request, self.template_name[0],
                      {'form': form})

    def post(self, request, recipe_id):
        recipe = get_object_or_404(RecipePost, id=recipe_id)
        form = self.form_class(request.POST, instance=recipe)
        if form.is_valid():
            recipe.save()
            return render(request, self.template_name[1])
        return render(request, self.template_name[0],
                      {'form': form})


def delete_recipe(request, recipe_id):
    recipe = RecipePost.objects.all().filter(pk=recipe_id,
                                             author=request.user)
    if recipe:
        recipe.delete()
        messages.success(request, 'Your recipe has been successfully deleted.')
    else:
        messages.error(request, 'This is not your recipe, you cannot delete it.')
    return render(request, 'cookbook/cookbook_list.html')
