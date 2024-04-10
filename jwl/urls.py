"""NFT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static

from trade_admin_auth.views import adminlogin

urlpatterns = [
    path('ZMXTASKmxuIRDREf/', admin.site.urls),
    
    re_path(r'^tradeadmin/',include("trade_admin_auth.urls" ,namespace="trade_admin_auth")),
    re_path(r'^trademaster/',include("trade_master.urls" ,namespace="trade_master")),
    re_path(r'^tradecurrency/',include("trade_currency.urls" ,namespace="trade_currency")),
    re_path(r'^themesettings/',include("themesettings.urls" ,namespace="themesettings")),
    re_path('W8n9cQU3MAh1mjhT', adminlogin, name='adminlogin'),
    re_path('',include("chit.urls" ,namespace="chit")),



    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)