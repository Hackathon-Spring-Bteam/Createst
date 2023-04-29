from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from .models import TestModel, LabelModel

from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

#testをリクエストするform
class TestModelForm(forms.ModelForm):
    FORMAT_CHOICES = (
        ('2', '2択問題'),
        ('4', '4択問題'),
    )

    test_format = forms.ChoiceField(
        choices=FORMAT_CHOICES,
        widget=forms.RadioSelect,
        label='形式',
    )

    class Meta:
        model = TestModel
        fields = ['test_title', 'test_keyword', 'label', 'test_format']
        labels = {
            'test_title': 'タイトル',
            'test_keyword': 'キーワード',
            'label': 'ラベル名',
        }

    def __init__(self, *args, **kwargs):
        super(TestModelForm, self).__init__(*args, **kwargs)
        self.fields['label'].queryset = LabelModel.objects.all()
        self.fields['label'].label_from_instance = lambda obj: f"{obj.label_name}"

class LoginForm(AuthenticationForm):
    # ログインフォーム
    pass

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(label="")
    password = forms.CharField(label="", widget=forms.PasswordInput())

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password']
        user = User.objects.get(id=self.user_id)
        if not authenticate(username=user.username, password=password):
            raise ValidationError('パスワードが間違っています。')
        return password

    def clean_new_username(self):
        new_username = self.cleaned_data['new_username']
        if User.objects.filter(username=new_username).exists():
            raise ValidationError('このアカウント名は既に使われています。')
        return new_username

    def save(self):
        user = User.objects.get(id=self.user_id)
        user.username = self.cleaned_data['new_username']
        user.save()

class ChangeEmailForm(forms.Form):
    current_email = forms.EmailField(label='')
    new_email = forms.EmailField(label='')
    password = forms.CharField(label='', widget=forms.PasswordInput())

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super().__init__(*args, **kwargs)

    def clean_current_email(self):
        current_email = self.cleaned_data['current_email']
        user = User.objects.get(id=self.user_id)
        if current_email != user.email:
            raise ValidationError('現在のメールアドレスが正しくありません。')
        return current_email

    def clean_new_email(self):
        new_email = self.cleaned_data['new_email']
        if User.objects.filter(email=new_email).exists():
            raise ValidationError('このメールアドレスは既に使われています。')
        return new_email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        user = authenticate(username=User.objects.get(id=self.user_id).username, password=password)
        if not user:
            raise ValidationError('パスワードが正しくありません。')
        return cleaned_data

    def save(self):
        user = User.objects.get(id=self.user_id)
        user.email = self.cleaned_data['new_email']
        user.save()

