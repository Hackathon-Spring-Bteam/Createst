from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm, TestModelForm,ChangeUsernameForm,ChangeEmailForm,ChangePasswordForm, LabelForm
from .models import TestModel, ProblemModel, ChoiceModel, LabelModel
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
import openai
from django.views.generic import TemplateView
import json
from django.contrib import messages
import time
from django.views.generic import ListView

# Index.html
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "index.html")

#プッシュする際はAPI KEYを必ず空にすること
openai.api_key = ''

# テストを生成するview
class CreateTestView(LoginRequiredMixin, TemplateView):
    template_name = "create.html"

    def get(self, request):
        form = TestModelForm()
        label_form = LabelForm()
        return render(request, "create.html", {"form": form, "label_form": label_form})
    
    def post(self, request):
        #フォームを処理
        form_type = request.POST.get('form_type')

        #formのvalueが'label_form'の場合ラベルを追加する処理
        if form_type == 'label_form':
            form = LabelForm(request.POST)
            if form.is_valid():
                label = form.save(commit=False)
                label.user = request.user
                label.save()
                return redirect('create')
            
        #formのvalueが'test_form'の場合、テストを生成する処理
        elif form_type == 'test_form':
            form = TestModelForm(request.POST)
            if form.is_valid():
                test = form.save(commit=False)
                test.user = request.user
                test.save()
            
        #難易度のリスト
        difficulties = ["really hard", "normal", "brainteaser"]
        
        #難易度をfor文で回してdifficultyに入れる
        for difficulty in difficulties[:3]:
            chat_input = f"grt qz based on kwd: {test.test_keyword}. qz must be academically challenging. difficulty: {difficulties}. inc correct ans amg 'choices_a' to 'choices_d'. 'answer' as the actual choice txt. For 2-ch quiz, grt 'problem_statement', 'answer', 'choices_a', and 'choices_b' in the indented JSON. For 4-ch quiz, grt 'problem_statement', 'answer', 'choices_a', 'choices_b', 'choices_c', and 'choices_d' in the indented JSON."
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": chat_input}
                ],
                max_tokens=500,
                n=1,
                temperature=0.2,
            )
            #APIからのリスポンスを解析
            response_text = response['choices'][0]['message']['content'].strip()
            
            response_json = json.loads(response_text)
            
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

        return redirect('test', test_id=test.test_id)

#生成したTESTを表示するview
class ShowQuizView(LoginRequiredMixin, View):
    def calculate_score_for_test(self, test):
        # テストに関連付けられた問題の数を取得
        total_questions = test.problemmodel_set.count()

        # ユーザーの回答が正解である回答（is_correct = True）の数を取得
        correct_answers = ProblemModel.objects.filter(test=test, is_correct=True).count()

        return correct_answers, total_questions

    def get(self, request, test_id):
        test = TestModel.objects.get(test_id=test_id)
        problems = ProblemModel.objects.filter(test=test)
        problem_choices = []
        for problem in problems:
            choices = ChoiceModel.objects.filter(problem=problem)
            problem_choices.append((problem, choices))
        score = test.score  # テストモデルからスコアを取得
        return render(request, "test.html", {"problem_choices": problem_choices, "score": score})  # スコアをテンプレートに渡す

    def post(self, request, test_id):
        if 'regenerate' in request.POST:
            old_test = TestModel.objects.get(test_id=test_id)

            # 新しいテストを作る際に生成済みのテストから、要素を取り出す
            new_test = TestModel.objects.create(test_format=old_test.test_format, test_keyword=old_test.test_keyword, user=request.user, label_id=old_test.label_id)

            #難易度のリスト
            difficulties = ["really hard", "normal", "brainteaser"]

            #難易度をfor文で回してdifficultyに入れる
            for difficulty in difficulties[:3]:
                chat_input = f"grt qz based on kwd: {test.test_keyword}. qz must be academically challenging. difficulty: {difficulties}. inc correct ans amg 'choices_a' to 'choices_d'. 'answer' as the actual choice txt. For 2-ch quiz, grt 'problem_statement', 'answer', 'choices_a', and 'choices_b' in the indented JSON. For 4-ch quiz, grt 'problem_statement', 'answer', 'choices_a', 'choices_b', 'choices_c', and 'choices_d' in the indented JSON."

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
                    return redirect('create')

                #以下DBに保存するコード
                problem_statement = response_json["problem_statement"]
                correct_answer = response_json["answer"]
                choices_a = response_json["choices_a"]
                choices_b = response_json["choices_b"]

                problem = ProblemModel.objects.create(problem_statement=problem_statement, correct_answer=correct_answer, test=new_test)
                ChoiceModel.objects.create(choice=choices_a, problem=problem)
                ChoiceModel.objects.create(choice=choices_b, problem=problem)

                if new_test.test_format == 4:
                    choices_c = response_json["choices_c"]
                    choices_d = response_json["choices_d"]
                    ChoiceModel.objects.create(choice=choices_c, problem=problem)
                    ChoiceModel.objects.create(choice=choices_d, problem=problem)

            # 新しいtest_idのページに遷移
            return redirect('test', test_id=new_test.test_id)

        # 再生成が選択されなかったときにユーザーの回答をDBに保存 & 得点を記録
        else:
            test = TestModel.objects.get(test_id=test_id)
            for key, value in request.POST.items():
                if key.startswith('user_answer_'):
                    problem_id_key = 'problem_id_' + key.split('_')[-1]
                    if problem_id_key in request.POST:
                        problem_id = request.POST[problem_id_key]
                        problem = ProblemModel.objects.get(problem_id=problem_id)
                        problem.user_answer = value
                        if value == problem.correct_answer:  # ユーザーの回答が正しい場合
                            problem.is_correct = True
                        else:  # ユーザーの回答が正しくない場合
                            problem.is_correct = False
                        problem.save()
            correct_answers, total_questions = self.calculate_score_for_test(test)
            score_str = f"{correct_answers}/{total_questions}"  # スコアを文字列形式で保存
            test.score = score_str  # テストのスコアを更新
            test.save()  # テストを保存してスコアをDBに保存
            return redirect('test', test_id=test_id)
       
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
    

class TestListView(ListView):
    model = TestModel
    template_name = 'index.html'
    context_object_name = 'test_list'

    def get_queryset(self):
        # ログインしているユーザーに紐づいたテストモデルを取得
        return TestModel.objects.filter(user=self.request.user)