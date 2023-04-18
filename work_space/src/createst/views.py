from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm, CustomForm
from .models import Test
from django.urls import reverse
from django.http import HttpResponseRedirect

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomForm()
        return render(request, 'form_template.html', {'form': form})

    def post(self, request):
        form = CustomForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            keyword = form.cleaned_data['keyword']
            radio_choice = form.cleaned_data['radio_choice']
            test = Test(title=title, keyword=keyword, radio_choice=radio_choice, user=request.user)
            test.save()
            return HttpResponseRedirect('/index/')
        return render(request, 'form_template.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
        return render(request, 'login.html', {'form': form})

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'signup.html', {'form': form})

class LogoutView(View):
    pass

class UserView(View):
    pass

class OtherView(View):
    pass