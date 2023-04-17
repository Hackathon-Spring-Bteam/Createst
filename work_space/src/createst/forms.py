from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class CustomForm(forms.Form):
    title = forms.CharField(label='タイトル', max_length=100)
    keyword = forms.CharField(label='キーワード', max_length=100)
    CHOICES = ((1, '1'), (2, '2'))
    radio_choice = forms.ChoiceField(label='選択', choices=CHOICES, widget=forms.RadioSelect)

class LoginForm(AuthenticationForm):
    # ログインフォーム
    pass

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']