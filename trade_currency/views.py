from django.shortcuts import render
from django.shortcuts import render,get_list_or_404, get_object_or_404


from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views.generic import TemplateView,View
from pycoingecko import CoinGeckoAPI


from django.http.response import HttpResponseRedirect
from django.http import HttpResponse,Http404
from django.urls import reverse
from django.urls import reverse_lazy
from django.template.context_processors import csrf
from django.shortcuts import redirect
from django.http import JsonResponse

from datetime import date,timedelta
import datetime


from decimal import *
from django.db.models import Q,F,Func,Value
from django.db.models import Count, Min,Max, Sum, Avg,DecimalField,DateTimeField,CharField
from django.db.models.expressions import RawSQL
from django.db.models.functions import Cast,TruncSecond,ExtractSecond


from django.db import transaction

from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.contrib import messages


from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required,user_passes_test
from django.core.exceptions import PermissionDenied
from auditable.views import AuditableMixin


from django_ajax.decorators import ajax


from django_tables2 import RequestConfig


from trade_admin_auth.mixins import check_group,ManageCurrencyAdminRequiredMixin

from trade_currency.models import TradeCurrency,TradePairs

from trade_currency.forms import  TradeCurrencyForm,TradePairsForm

from trade_currency.cron import cron_currency_api,checkcron_currency_api


class Listtradecurrency(ListView):
    model = TradeCurrency
    template_name = 'trade_currency/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return TradeCurrency.objects.filter(status=0)
    def get_context_data(self,**kwargs):
        context=super(Listtradecurrency, self).get_context_data(**kwargs)
        context['Title'] = 'Currency List'
        content_qs = TradeCurrency.objects.filter(status=0)
        context['content_qs'] =content_qs
        contenttable = TradeCurrencyTable(content_qs)
        context['table'] = contenttable
        context['activecls']='currencydetailadmin'
        context['add_title'] ='Add Currency'
        context['Btn_url'] = 'trade_currency:addcurrency'
        return context


class Add_tradecurrency(CreateView):
    model = TradeCurrency
    form_class = TradeCurrencyForm
    template_name = 'trade_currency/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(Add_tradecurrency, self).get_context_data(**kwargs)
       context['Title'] = 'Add Currency'
       context['Btn_url']='trade_currency:currencylist'
       context['activecls']='currencydetailadmin'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.created_by_id = self.request.user.id
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Currency created successfully.')
       return HttpResponseRedirect('/tradecurrency/currencylist/')


class Update_tradecurrency(UpdateView):
    model = TradeCurrency
    form_class = TradeCurrencyForm
    template_name = 'trade_currency/currencyedit_form.html'  
    def get_context_data(self, **kwargs):
       context = super(Update_tradecurrency, self).get_context_data(**kwargs)
       context['Title'] = 'Edit Currency'
       context['Btn_url']='trade_currency:currencylist'
       context['activecls']='currencydetailadmin'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'currency updated successfully.')
       return HttpResponseRedirect('/tradecurrency/currencylist/')



class Listtradepair(ListView):
    model = TradePairs
    template_name = 'trade_currency/tradepairlist.html'
    def get_queryset(self, **kwargs):
      return TradePairs.objects.all()
    def get_context_data(self,**kwargs):
        context=super(Listtradepair, self).get_context_data(**kwargs)
        context['Title'] = 'Pairs List'
        content_qs = TradePairs.objects.all()
        context['content_qs'] =content_qs
        contenttable = TradePairsTable(content_qs)
        context['table'] = contenttable
        context['activecls']='currencydetailadmin'
        context['add_title'] ='Add Pair'
        context['Btn_url'] = 'trade_currency:addpair'
        return context


class Add_tradepair(CreateView):
    model = TradePairs
    form_class = TradePairsForm
    template_name = 'trade_currency/currencyform.html'   
    def get_context_data(self, **kwargs):
       context = super(Add_tradepair, self).get_context_data(**kwargs)
       context['Title'] = 'Add Pair'
       context['Btn_url']='trade_currency:tradepairlist'
       context['activecls']='currencydetailadmin'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       form.instance.created_by_id = self.request.user.id
       form.instance.margin_loan_duration=0
       form.instance.margin_loan_rate=0
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Pairs created successfully.')
       return HttpResponseRedirect('/tradecurrency/tradepairlist/')

class Update_tradepair(UpdateView):
    model = TradePairs
    form_class = TradePairsForm
    template_name = 'trade_currency/currencyform.html'   
    def get_context_data(self, **kwargs):
       context = super(Update_tradepair, self).get_context_data(**kwargs)
       context['Title'] = 'Edit Pair'
       context['Btn_url']='trade_currency:tradepairlist'
       context['activecls']='currencydetailadmin'
       return context

    @transaction.atomic
    def form_valid(self, form):
       
       form.instance.modified_by_id = self.request.user.id
       form.instance.created_by_id = self.request.user.id
       form.instance.margin_loan_duration=0
       form.instance.margin_loan_rate=0
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Pairs updated successfully.')
       return HttpResponseRedirect('/tradecurrency/tradepairlist/')
 
def check_currencyapi(request):
  cron_currency_api(request)
  return HttpResponseRedirect('/')  


@ajax
def getmarketprice_ajax(request):
    try:
      marketpricelistdata = TradePairs.objects.all()
      marketpricelist = []
      i=0
      for item in marketpricelistdata:
        market_temp = {}
        i = i+1
        market_temp['count']= i
        market_temp['price_id'] = item.id
        market_temp['pairname'] = item.pair_name
        market_temp['marketprice'] = round(Decimal(item.last_price),2)
        market_temp['status'] = item.get_status_display() 
        marketpricelist.append(market_temp)
      return JsonResponse({'status':'success','msg':'success','marketdatalist':marketpricelist})
    except Exception as e:
      marketpricelist = ''
      return  JsonResponse({'status':'Failed','msg':'failed','marketdatalist':marketpricelist})





