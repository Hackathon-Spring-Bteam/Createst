from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from .models import TestModel

#form
class CustomForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ['test_title', 'test_format', 'test_keyword', 'label']
        
        labels = {
                'test_title': 'タイトル',
                'test_format': '形式',
                'test_keyword': 'キーワード',
                'label': 'ラベル'
        }

class LoginForm(AuthenticationForm):
    # ログインフォーム
    pass

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']