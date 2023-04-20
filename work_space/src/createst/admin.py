from django.contrib import admin
from .models import LabelModel, TestModel, ProblemModel, ChoiceModel

admin.site.register(LabelModel)
admin.site.register(TestModel)
admin.site.register(ProblemModel)
admin.site.register(ChoiceModel)