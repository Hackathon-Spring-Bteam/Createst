from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm, TestModelForm,ChangeUsernameForm,ChangeEmailForm
from .models import TestModel
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from django.contrib import messages

#Index.html
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'index.html')

#テストをリクエストするフォーム & 送信でindexに遷移
class TestView(LoginRequiredMixin, CreateView):
    model = TestModel
    template_name = 'test_form.html'
    form_class = TestModelForm
    success_url = '/index/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        test = form.save()
        test.user = self.request.user
        test.save()
        return HttpResponseRedirect(self.success_url)

#login.html
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

#Signup.html
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

#logout機能
class LogoutView(View):
    pass

class UserView(View):
    pass

class OtherView(View):
    pass

class ChangeUsernameView(LoginRequiredMixin, View):
    form_class = ChangeUsernameForm
    template_name = 'usernameup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(user_id=request.user.id)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(user_id=request.user.id, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'アカウント名を変更しました。')
            return redirect('/index/')
        context = {'form': form}
        return render(request, self.template_name, context)
    
class ChangeEmailView(LoginRequiredMixin, View):
    form_class = ChangeEmailForm
    template_name = 'Emailup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class(user_id=request.user.id)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(user_id=request.user.id, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'メールアドレスを変更しました。')
            return redirect('/home/')
        return render(request, self.template_name, {'form': form})