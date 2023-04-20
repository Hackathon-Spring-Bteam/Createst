from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from .models import TestModel, LabelModel

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