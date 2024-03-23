from django.contrib import admin
from core.models.AnswerTemplateQuestions import AnswerTemplateQuestions

from core.models.Patient import Patient
from .models.role import Role
# from .model import user
from .models.AssignedRule import AssignedRule
from .models.Questions import Questions
from .models.AnswerTemplateQuestions import AnswerTemplateQuestions


admin.site.register(Role)
admin.site.register(AssignedRule)
admin.site.register(Patient)
admin.site.register(AnswerTemplateQuestions)


 

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('title','question_text', 'type', 'order', 'group','page', 'active')
    list_filter = ('type','page', 'active')
    search_fields = ('title','question_text')
