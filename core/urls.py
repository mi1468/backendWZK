from django.urls import re_path
from django.contrib import admin
from django.urls import path

from . import views
from .views import patientView
from .views import TemplateQuestionsView
from .views import AnswerTemplateQuestionsView

urlpatterns = [

    path('admin/', admin.site.urls),


    re_path('signup', patientView.signup),
    re_path('login', patientView.login),
    re_path('getInfo', patientView.getInfo),

    re_path('sendSmsVerification', patientView.sendSmsVerification),
    re_path('sendEmailVerification', patientView.sendEmailVerification),
    re_path('submitEmailVerification', patientView.submitEmailVerification),

    re_path('test_token_admin', patientView.test_token),


    re_path('templatequestions', TemplateQuestionsView.get_template_questions),
    re_path('templatepages', TemplateQuestionsView.get_template_pages),
    re_path('savetemplateform', AnswerTemplateQuestionsView.submit_answer),

    
    re_path('templatequestionscgm', TemplateQuestionsView.get_template_questions_cgm),



    # path('templatequestions/', get_template_questions , name='template_questions_api'),

]
