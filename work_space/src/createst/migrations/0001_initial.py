# Generated by Django 3.2.18 on 2023-04-17 13:08

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('label_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('label_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='createst_user_groups', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='このユーザーに対する特定の権限。', related_name='createst_user_set', related_query_name='user', to='auth.Permission', verbose_name='ユーザー権限')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('test_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('test_title', models.CharField(max_length=50)),
                ('test_format', models.CharField(max_length=50)),
                ('test_keyword', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('prompt', models.CharField(max_length=50)),
                ('public_key', models.BooleanField(default=True)),
                ('test_status', models.IntegerField(choices=[(1, 'Status 1'), (2, 'Status 2')])),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createst.label')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createst.user')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('problem_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('problem_statement', models.CharField(max_length=200)),
                ('correct_answer', models.CharField(max_length=50)),
                ('user_answer', models.CharField(blank=True, max_length=50, null=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createst.test')),
            ],
        ),
        migrations.AddField(
            model_name='label',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createst.user'),
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('choice_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('choice', models.CharField(max_length=50)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createst.problem')),
            ],
        ),
    ]