from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()

class LabelModel(models.Model):
    label_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class TestModel(models.Model):
    #2択か4択のどちらかを保存
    FORMAT_CHOICES = (
        (2, '2択問題'),
        (4, '4択問題'),
    )
    test_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_title = models.CharField(max_length=50)
    test_format = models.IntegerField(choices=FORMAT_CHOICES)
    test_keyword = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    public_key = models.BooleanField(default=True)
    label = models.ForeignKey(LabelModel, on_delete=models.CASCADE)
    score = models.CharField(max_length=50, default="0/3")

class ProblemModel(models.Model):
    problem_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem_statement = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=50)
    user_answer = models.CharField(max_length=50, blank=True, null=True)
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE)
    #正誤判定機能
    is_correct = models.BooleanField(default=None, null=True, blank=True)

class ChoiceModel(models.Model):
    choice_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice = models.CharField(max_length=50)
    problem = models.ForeignKey(ProblemModel, on_delete=models.CASCADE)