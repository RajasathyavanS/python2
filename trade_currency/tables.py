import django_tables2 as tables
from django_tables2.utils import A

from datetime import date
from django.db.models import Q

from django.contrib.auth.models import User

import itertools
from trade_currency.models import TradeCurrency,TradePairs



class TradeCurrencyTable(tables.Table):
     
     BUTTON_TEMPLATE = """
       
        <a href="{% url 'trade_currency:edit_currency' record.pk %}" title="Edit" class="btn"><i class="fa fa-edit"></i></a>
      
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)
     class Meta:
         model =  TradeCurrency
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','type_currncy','name','symbol','address','status','Actions']




class TradePairsTable(tables.Table):
     
     BUTTON_TEMPLATE = """
      
        <a href="{% url 'trade_currency:edit_tradepair' record.id %}" title="Edit" class="btn"><i class="fa fa-edit"></i></a>
      
      
     """
     Lastprice_TEMPLATE = """ {% if record.currencytype.currncytype == 0  %}
                {{ record.last_price|floatformat:-2}}
              {% else %}
                {{ record.last_price|floatformat:-2}}
              {% endif%}
     """
     Change_price_TEMPLATE = """ {% if record.currencytype.currncytype == 0  %}
                {{ record.change_price|floatformat:-2}}
              {% else %}
                {{ record.change_price|floatformat:-2}}
              {% endif%}
     """
     Volume_price_TEMPLATE = """ {% if record.currencytype.currncytype == 0  %}
                {{ record.volume_price|floatformat:-8}}
              {% else %}
                {{ record.volume_price|floatformat:-8}}
              {% endif%}
     """

     last_price = tables.TemplateColumn(Lastprice_TEMPLATE )
     
     
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)
     class Meta:
         model =  TradePairs
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','pair_name','last_price','status','Actions']


         


class Farm_addTable(tables.Table):
     
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)
     class Meta:
         model =  Stack_Farming
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','pair','allocation','pools_id','created_on','status']   

