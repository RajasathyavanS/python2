from django.contrib import admin
from django.urls import include, path
from chit import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from themesettings import views as v1

from . import views

from django.views.decorators.csrf import csrf_exempt

app_name = 'Chit'

loginurl='/W8n9cQU3MAh1mjhT/'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('otp_verfication/', views.otp_verfication, name='otp_verfication'),
    path('create_mpin/', views.create_mpin, name='create_mpin'),
    path('mpin_verfication/', views.mpin_verfication, name='mpin_verfication'),
    path('forget_mpin/', views.forget_mpin, name='forget_mpin'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('user_login/', views.user_login, name='user_login'),
    path('encrypt/<str:input>/', views.encrypt, name='encrypt'),
    path('decrypt/<str:input>/', views.decrypt, name='decrypt'),


    
    
    
    
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)