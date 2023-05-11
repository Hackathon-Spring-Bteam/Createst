from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm, TestModelForm,ChangeUsernameForm,ChangeEmailForm,ChangePasswordForm
from .models import TestModel
from .forms import LoginForm, SignupForm, TestModelForm
from .models import TestModel, ProblemModel, ChoiceModel
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
import openai
from django.views.generic import TemplateView
import json
from django.contrib import messages
import time

#Index.html
# Index.html
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "index.html")
    
openai.api_key = "API_KEY"

# テストを生成するview
class CreateTestView(LoginRequiredMixin, TemplateView):
    template_name = "create.html"

    def get(self, request):
        form = TestModelForm()
        return render(request, "create.html", {"form": form})

    def post(self, request):
        form = TestModelForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.user = request.user
            test.save()
            
            #難易度のリスト
            difficulties = ["easy", "normal", "hard", "super_hard", "brainteaser"]
            
            #難易度をfor文で回してdifficultyに入れる
            for difficulty in difficulties[:3]:
                chat_input = f"Crt {test.test_format}-ch qz qstn kwd: {test.test_keyword}. Qz dfclty: {difficulty}. Outpt: indntd JSON. NO excpt JSON. Incld crct ans in chcs 'a'-'d'. 'ans' is crct ans, 'a'-'d' are chcs. 'problem_statement', 'answer', 'choices_a', and 'choices_b' is for 2-ch qz. 'problem_statement', 'answer', 'choices_a', 'choices_b', 'choices_c', and 'choices_d' is for 4-ch qz.Gnt prblm reltd to kwd: {test.test_keyword}. Chcs 'a'-'d' no ovrlp. No ez or inacc prblms."
                
                #APIの設定
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": chat_input}
                    ],
                    max_tokens=500,
                    n=1,
                    temperature=0.3,
                )
                #APIからのリスポンスを解析
                response_text = response['choices'][0]['message']['content'].strip()
                
                #うまくJSONを取得できなかった時の例外処理
                try:
                    response_json = json.loads(response_text)
                except json.JSONDecodeError:
                    messages.error(request, f'エラーが発生しました。キーワードを正確に入力してください。Response: {response_text}')
                    return render(request, "create.html", {"form": form, "response_text": response_text})
                
                #以下DBに保存するコード
                problem_statement = response_json["problem_statement"]
                correct_answer = response_json["answer"]
                choices_a = response_json["choices_a"]
                choices_b = response_json["choices_b"]

                problem = ProblemModel.objects.create(problem_statement=problem_statement, correct_answer=correct_answer, test=test)
                ChoiceModel.objects.create(choice=choices_a, problem=problem)
                ChoiceModel.objects.create(choice=choices_b, problem=problem)

                if test.test_format == 4:
                    choices_c = response_json["choices_c"]
                    choices_d = response_json["choices_d"]
                    ChoiceModel.objects.create(choice=choices_c, problem=problem)
                    ChoiceModel.objects.create(choice=choices_d, problem=problem)

                # debug用に一時的にresponseを保存
                request.session['response_text'] = response_text

            return redirect('test', test_id=test.test_id)

#生成したTESTを表示するview
class ShowQuizView(LoginRequiredMixin, View):
    def get(self, request, test_id):
        test = TestModel.objects.get(test_id=test_id)
        problems = ProblemModel.objects.filter(test=test)
        problem_choices = []
        for problem in problems:
            choices = ChoiceModel.objects.filter(problem=problem)
            problem_choices.append((problem, choices))
        
        #debug用
        response_text = request.session.get('response_text', None)
        return render(request, "test.html", {"problem_choices": problem_choices, "response_text": response_text}) #response_textはdebug用

# login.html
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        return render(request, "login.html", {"form": form})

# Signup.html
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login"))
        return render(request, "signup.html", {"form": form})

# logout機能
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
            return redirect('/index/')
        return render(request, self.template_name, {'form': form})
    
class ChangePasswordView(LoginRequiredMixin,View):
    template_name = 'passwordup.html'
    form_class = ChangePasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user.id)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user.id, data=request.POST)
        if form.is_valid():
            # 新しいパスワードをセットする
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            # ユーザーを再認証してログインする
            user = authenticate(username=user.username, password=form.cleaned_data['new_password'])
            if user is not None:
                login(request, user)

            messages.success(request, 'パスワードを変更しました。')
            return redirect('/index/')
        return render(request, self.template_name, {'form': form})