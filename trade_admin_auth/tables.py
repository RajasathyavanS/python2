import django_tables2 as tables
from django_tables2.utils import A
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import django_filters
from django_filters import DateRangeFilter,DateFilter
from django import forms
from datetime import date
from django.db.models import Q
import itertools

from django.contrib.auth.models import User

from trade_admin_auth.models import AdminUser_Profile,AdminUser_Activity

from trade_master.models import Blockip
#from trade_auth.models import UserAddress

def next_count():
    return next(counter)

         

class DeactivateUserTable(tables.Table):
     
     class Meta:
         model =  User
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example'}
         fields=['username','email','is_active','']        

class DashboardAdminActivityTable(tables.Table):
     
     class Meta:
         model =  AdminUser_Activity
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['user','ip_address','activity','browsername','os','devices','created_on']

class AdminActivityTable(tables.Table):
     counter = tables.Column(empty_values=(),verbose_name='S.No', orderable=False)
     def render_counter(self):
      self.row_counter = getattr(self, 'row_counter', itertools.count(self.page.start_index()))
      return next(self.row_counter)
     class Meta:
         model =  AdminUser_Activity
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example'}
         fields=['counter','user','ip_address','activity','browsername','os','devices','created_on']

class AdminActivityTableFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all(),label ='Client Name')
    
    class Meta:
        model = AdminUser_Activity
        fields=['user']
class AdminActivitySearch_Form(FormHelper):
        model = AdminUser_Activity
        form_id = 'Bill_Search_Form'
        form_method = 'get'
        form_class = 'form-horizontal'
        form_role = 'form'
        label_class = 'col-md-3'
        field_class = 'col-md-5'



class BlockIPTable(tables.Table):
     
     BUTTON_TEMPLATE = """

        <a href="/tradeadmin/editblockip/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Blockip
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','ip_address','ip_level','status'] 

'''
class UserAddressTable(tables.Table):
     BUTTON_TEMPLATE = """

        <a href="/tradeadmin/walletdetail/{{record.id}}/" title="Edit"><i class="fa fa-info"></i></a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )

     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',) 
     class Meta:
         model =  UserAddress
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','useraddress','created_on','modified_on']
'''

class SubAdminTable(tables.Table):
     BUTTON_TEMPLATE = """

        <a href="/tradeadmin/sub_admin_profile_settings/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     
     row_number = tables.Column(empty_values=())
     class Meta:
         model =  User
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['row_number','username','email','date_joined','is_active'] 