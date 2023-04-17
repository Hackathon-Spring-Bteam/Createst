from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_query_name="user",
        related_name="createst_user_groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name="user",
        related_name="createst_user_permissions",
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='ユーザー権限',
        blank=True,
        help_text='このユーザーに対する特定の権限。',
        related_query_name="user",
        related_name="createst_user_set",
    )

class Label(models.Model):
    label_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Test(models.Model):
    test_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_title = models.CharField(max_length=50)
    test_format = models.CharField(max_length=50)
    test_keyword = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    prompt = models.CharField(max_length=50)
    public_key = models.BooleanField(default=True)
    test_status_choices = (
        (1, 'Status 1'),
        (2, 'Status 2'),
        # 他に許可されるステータスがあれば追加する
    )
    test_status = models.IntegerField(choices=test_status_choices)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

class Problem(models.Model):
    problem_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem_statement = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=50)
    user_answer = models.CharField(max_length=50, blank=True, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Choice(models.Model):
    choice_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice = models.CharField(max_length=50)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)