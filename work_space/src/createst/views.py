from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm, CustomForm
from .models import TestModel
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomForm()
        return render(request, 'index.html', {'form': form})

#テストをリクエストするフォーム
class TestView(LoginRequiredMixin, CreateView):
    model = TestModel #追記
    template_name = 'test_form.html'     
    # form = CustomForm
    fields = ['test_title', 'test_format', 'test_keyword', 'label']
    success_url = '/index/'

    def form_valid(self, form):
        form.instance.user = self.request.user #追記
        test = form.save()
        test.user = self.request.user
        test.save()
        return HttpResponseRedirect(self.success_url)

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