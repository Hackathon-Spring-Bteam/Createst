from django.contrib import admin
from .models import Label, User, Test, Problem, Choice

admin.site.register(Label)
admin.site.register(User)
admin.site.register(Test)
admin.site.register(Problem)
admin.site.register(Choice)