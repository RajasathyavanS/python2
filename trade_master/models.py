from django.db import models

from django.conf import settings


from datetime import date

from django.core.validators import RegexValidator
from auditable.models import Auditable

from django.urls import reverse
import os
from django.db.models import Q
from django.db.models import Count, Min, Sum, Avg ,F,DecimalField
from decimal import Decimal
import time

from django.utils import timezone

from ckeditor.fields import RichTextField



General_Status = (
					(0,'Active'),
					(1,'Inactive'),
					
	)

ip_type = (
	(0,'User'),
	(1,'Admin'),
					
	)

Content_type = (
	(0,'page'),
	(1,'content')

	)
Read_Status = (
	(0,'UnReply'),
	(1,'Replied')
	)

class Cms_StaticContent(Auditable):
	name = models.CharField(max_length=50,verbose_name='Name',blank=True,null=True)
	title = models.CharField(max_length=50,verbose_name='Title')
	content = RichTextField(help_text='Content',verbose_name='Content',blank=True,null=True)
	contenttype=models.IntegerField(choices=Content_type,default=0,verbose_name='Content')
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='Cms_StaticContent'
		db_table='C9bDIAkN3dlB5T1b'


class Faq(Auditable):
	title = models.CharField(max_length=100,verbose_name='Question')
	content = models.TextField(help_text='Content',verbose_name='Content',blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='Faq'
		db_table='fOfwvYRmmHVwm48s'


class Roadmap(Auditable):
	title = models.CharField(max_length=50,verbose_name='Title')
	year = models.CharField(max_length=50,verbose_name='Year')
	content = models.TextField(help_text='Content',verbose_name='Content',blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='Roadmap'
		db_table='RQ99aE1KxKWQ2o1D'


class Contactus(models.Model):

	phone1=models.CharField(max_length=13,verbose_name='Phone Number',blank=True,null=True)
	name =models.CharField(max_length=50,verbose_name='Name')
	email = models.CharField(max_length=50,verbose_name='Email')
	subject = models.CharField(max_length=50,verbose_name='Subject')
	message = models.TextField(help_text='Message',verbose_name='Message')
	reply = models.TextField(help_text='Message',verbose_name='Reply',blank=True,null=True)
	status =models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	read_status =models.IntegerField(choices=Read_Status,default=0,verbose_name='Read Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	def __int__self(self):
		return id
	class Meta:
		verbose_name='Contactus'
		db_table='cSlmuii55R4oLi9Q'


class EmailTemplate(Auditable):
	
	name = models.CharField(max_length=50,verbose_name='Name')
	Subject = models.CharField(max_length=300,verbose_name='Subject')
	content = RichTextField(help_text='Content',verbose_name='Content')
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='EmailTemplate'
		db_table='E5w4yMqjVXoTQlty'



class Currencylist(Auditable):
	name = models.CharField(max_length=50,verbose_name='Name')
	softcap = models.CharField(max_length=50,verbose_name='Soft cap')
	hardcap = models.CharField(max_length=50,verbose_name="Hard cap")
	attachement = models.FileField(verbose_name='WhitePaper',blank=True,null=True)
	timer_date = models.DateTimeField()
	buytoken_url = models.CharField(max_length=100,verbose_name="Buy Token Url",blank=True,null=True)
	content = models.TextField(help_text='Content',verbose_name='Content',blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='Currencylist'
		db_table='c2plLP6av1pk3STI'



class Blockip(Auditable):
	ip_address = models.GenericIPAddressField()
	ip_option = models.IntegerField(choices=ip_type,default=0,verbose_name="IP Option")
	ip_level = models.CharField(max_length=50,verbose_name='Ip Level',blank=True,null=True)
	status = models.IntegerField(choices=General_Status,default=0,verbose_name="Status")
	
	def __int__self(self):
		return id

	class Meta:
		verbose_name='Blockip'
		db_table = 'BjRI3yQGhisBCfnZ'



class AccessLog(Auditable):
	Type = models.CharField(max_length=50,verbose_name='Type')
	name = models.CharField(max_length=50,verbose_name='Name',blank=True,null=True)
	title = models.CharField(max_length=50,verbose_name='Title')
	content = models.TextField(help_text='Content',verbose_name='Content',blank=True,null=True)
	datetime = models.DateTimeField(default=timezone.now)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='AccessLog'
		db_table='AbFQAh45sPZK86hd'