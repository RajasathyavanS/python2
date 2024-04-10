from django.urls import include, path,re_path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
app_name = 'trade_currency'

from . import views
from .views import Listtradepair,Update_tradepair,Add_tradepair
from .views import  Listtradecurrency,Update_tradecurrency,Add_tradecurrency



loginurl='/W8n9cQU3MAh1mjhT/'

urlpatterns = [
	
	 re_path(r'^addcurrency/$', login_required(Add_tradecurrency.as_view(),login_url=loginurl), name='addcurrency'),	
	 re_path(r'^edit_currency/(?P<pk>[-\w]+)/$', login_required(Update_tradecurrency.as_view(),login_url=loginurl), name='edit_currency'),
	 re_path(r'^currencylist/$', login_required(Listtradecurrency.as_view(),login_url=loginurl), name='currencylist'),

	 re_path(r'^addpair/$', login_required(Add_tradepair.as_view(),login_url=loginurl), name='addpair'),
	 re_path(r'^edit_tradepair/(?P<pk>[-\w]+)/$', login_required(Update_tradepair.as_view(),login_url=loginurl), name='edit_tradepair'),
	 re_path(r'^tradepairlist/$', login_required(Listtradepair.as_view(),login_url=loginurl), name='tradepairlist'),
	 
	 re_path(r'^marketprice/$', views.check_currencyapi, name='marketprice'),
	 re_path(r'^getmarketprice_ajax', csrf_exempt(views.getmarketprice_ajax), name='getmarketprice_ajax'),
	


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)