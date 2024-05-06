from django.contrib import admin

# Register your models here.
from clinet_patient_form.models.Questions import Questions
from clinet_patient_form.models.AnswerTemplateQuestions import AnswerTemplateQuestions
 
admin.site.register(AnswerTemplateQuestions)


 

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('title','question_text', 'type', 'order', 'group','page', 'active')
    list_filter = ('type','page', 'active')
    search_fields = ('title','question_text')
