from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm
from django.views.generic import View


# tested
from .services import user_register


class UserLogin(View):
    form_class = LoginForm
    template_name = ['cookbook/user_cookbook.html', 'account/login.html']

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect('cookbook:user_cookbook')
        return render(request, self.template_name[1], {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        template = self.template_name[1]
        context = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect('cookbook:user_cookbook')
            else:
                template = self.template_name[1]
                context = {'form': form, 'section': 'no_user'}

        return render(request, template, context)


def user_logout(request):
    logout(request)
    return render(request,
                  'registration/logged_out.html', )


# Tested
class UserRegister(View):
    form_class = UserRegistrationForm
    template_name = ['account/register.html', 'account/register_done.html']

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('cookbook:user_cookbook')
        user_form = self.form_class()
        return render(request, self.template_name[0],
                      {'user_form': user_form})

    def post(self, request):
        user_form = self.form_class(request.POST)
        template = self.template_name[0]
        context = {'user_form': user_form}
        if user_form.is_valid():
            new_user = user_register(user_form)
            template = self.template_name[1]
            context = {'new_user': new_user}

        return render(request, template, context)
