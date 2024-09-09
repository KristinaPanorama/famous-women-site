from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from sitewomen import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    extra_context = {'title': "Авторизация"}


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['login'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', context={'form': form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль', 'default_img': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Сменить пароль'}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

