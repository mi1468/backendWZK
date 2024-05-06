from django.urls import re_path
from django.contrib import admin
from django.urls import path
 
from .views import userView 
from django.urls import include, path

urlpatterns = [

    path('admin/', admin.site.urls),


    # re_path(r'^signup/$', userView.signup, name="signup"),
 
    re_path('signup', userView.signup , name="signup"),
    re_path('login', userView.login),
    re_path('getInfo', userView.getInfo),

    re_path('sendSmsVerification', userView.sendSmsVerification),
    re_path('sendEmailVerification', userView.sendEmailVerification),
    re_path('submitEmailVerification', userView.submitEmailVerification),

    re_path('sendForgetPasswordCode', userView.sendForgetPasswordCode),
    re_path('sendCodeAndNewPassword', userView.sendCodeAndNewPassword),

    path('clinet_patient_form/', include('clinet_patient_form.urls')),


   
   
]
