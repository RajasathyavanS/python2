import django_tables2 as tables
from django_tables2.utils import A

from datetime import date
from django.db.models import Q

from django.contrib.auth.models import User


from trade_master.models import Cms_StaticContent,Faq,Contactus,EmailTemplate
from trade_master.models import Roadmap,Currencylist,AccessLog


class StaticContentTable(tables.Table):
     
     BUTTON_TEMPLATE = """
        <a href="{% url 'trade_master:cms_page' record.id %}" title="Edit" class="btn"><i class="fa fa-edit"></i></a>
       <a href="{% url 'trade_master:cms_page_detail' record.id %}" title="Detail" class="btn"><i class="fa fa-info"></i></a>
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)
     class Meta:
         model =  Cms_StaticContent
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','title','Actions']

class CmsContentTable(tables.Table):
     
     BUTTON_TEMPLATE = """
        <a href="{% url 'trade_master:cms_content' record.id %}" title="Edit" class="btn"><i class="fa fa-edit"></i></a> 
       <a href="{% url 'trade_master:cms_page_contentdetail' record.id %}" title="Detail" class="btn"><i class="fa fa-info"></i></a>
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',) 
     class Meta:
         model =  Cms_StaticContent
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','title','Actions']



class FaqTable(tables.Table):
     
     BUTTON_TEMPLATE = """
        <a href="{% url 'trade_master:updatefaq' record.id %}" title="Edit" class="btn"><i class="fa fa-edit"></i></a>
       <a href="{% url 'trade_master:detail_faq' record.id %}" title="Detail" class="btn"><i class="fa fa-info"></i></a>
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',) 
     class Meta:
         model =  Faq
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','title','content','status','Actions']

class RoadmapTable(tables.Table):
     
     BUTTON_TEMPLATE = """
        <a href="{% url 'trade_master:updateroadmap' record.id %}" title="Edit" class="btn"><i class="fa fa-edit"></i></a>
       <a href="{% url 'trade_master:roadmapdetail' record.id %}" title="Detail" class="btn"><i class="fa fa-info"></i></a>
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',) 
     class Meta:
         model =  Roadmap
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','title','year','status','Actions']

class CurrencyTable(tables.Table):
     
     BUTTON_TEMPLATE = """
        <a href="{% url 'trade_master:updatecurrency' record.id %}" title="Edit" class="btn"><i class="fa fa-edit"></i></a>
       <a href="{% url 'trade_master:currencydetail' record.id %}" title="Detail" class="btn"><i class="fa fa-info"></i></a>
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',) 
     class Meta:
         model =  Currencylist
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','name','softcap','hardcap','timer_date','Actions']


class ContactusTable(tables.Table):
     
     BUTTON_TEMPLATE = """
       {% if record.get_read_status_display == "UnReply" %}
        <a href="{% url 'trade_master:contactus_update' record.id %}" title="Edit" class="btn"><i class="fa fa-edit"></i></a>
       {% else %}
       <a href="{% url 'trade_master:contactusdetail' record.id %}" title="Detail" class="btn"><i class="fa fa-info"></i></a>
       {% endif %}
       
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',) 
     class Meta:
         model =  Contactus
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','name','email','subject','read_status','created_on','modified_on','Actions']

class EmailTemplateTable(tables.Table):
     
     BUTTON_TEMPLATE = """
        <a href="{% url 'trade_master:emailcontent_update' record.id %}" title="Edit" class="btn"><i class="fa fa-edit"></i></a>
       
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)
     class Meta:
         model =  EmailTemplate
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','name','Subject','Actions']

