from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.views.generic import View
from django.contrib.auth.decorators import login_required


class UserLogin(View):

    template_name = ['account/user_cookbook.html', 'account/login.html']

    def get(self, request):
        form = LoginForm()
        # if request.user.is_authenticated():
        #     return HttpResponse('Successful')
        return render(request, self.template_name[1], {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request,
                                  self.template_name[0],
                                  {'section': 'user_cookbook'})
            else:
                return render(request, self.template_name[1], {'form': form, 'section': 'no_user'})
        else:
            form = LoginForm()
        return render(request, self.template_name[1], {'form': form})


def user_logout(request):
    logout(request)
    return render(request,
                  'registration/logged_out.html',)

#
# class UserLogout(View):
#     def logout(self):
#         return super().logout()


@login_required
def user_cookbook(request):
    return render(request,
                  'account/user_cookbook.html',
                  {'section': 'user_cookbook'})
