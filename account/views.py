from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm
from django.views.generic import View


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
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('cookbook:user_cookbook')
            else:
                return render(request, self.template_name[1],
                              {'form': form, 'section': 'no_user'})
        return render(request, self.template_name[1], {'form': form})


def user_logout(request):
    logout(request)
    return render(request,
                  'registration/logged_out.html', )


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
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set a chosen password. set_password added encryption.
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, self.template_name[1],
                          {'new_user': new_user})

        return render(request, self.template_name[0],
                      {'user_form': user_form})
