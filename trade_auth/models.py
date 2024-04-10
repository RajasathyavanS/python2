from django.db import models
from django.conf import settings

from django.contrib.auth.models import User,Group

from auditable.models import Auditable

from datetime import date

from django.core.validators import RegexValidator
import uuid
import os

from django.urls import reverse
import os
from django.db.models import Q
from django.db.models import Count, Min, Sum, Avg ,F,DecimalField
from decimal import Decimal
import time
from simple_history.models import HistoricalRecords

from trade_currency.models import TradeCurrency

Address_Status = (
		(0,'Active'),
		(1,'Inactive'),
		(2,'Cancelled')
	)
# Create your models here.
class UserAddress(models.Model):
	useraddress = models.CharField(max_length=100,verbose_name='Address')
	userbtcaddress = models.CharField(max_length=100,verbose_name='BTC Address',blank=True,null=True)
	contractid=models.IntegerField(verbose_name='Contract ID',default=0)
	status=models.IntegerField(choices=Address_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True,verbose_name='Created on')
	modified_on = models.DateTimeField(auto_now=True,verbose_name='Last Login')
	chainid=models.CharField(max_length=100,verbose_name='Chain_id',blank=True,null=True)
	wallet=models.CharField(max_length=100,verbose_name='Wallet',blank=True,null=True)
	select_token=models.CharField(max_length=120,null=True,blank=True,verbose_name='Select Token')
	select_id=models.CharField(max_length=120,null=True,blank=True,verbose_name='Select Id')
	def __str__(self):
		return self.useraddress
	class Meta:
		verbose_name = 'Useraddress'
		db_table ='APLegJVs5IOqnDex'



class UserWallet(models.Model):
	useraddress = models.ForeignKey(UserAddress,related_name ='userwalletaddress',on_delete=models.CASCADE,verbose_name='Address')
	currency = models.ForeignKey(TradeCurrency,related_name ='Currency',on_delete=models.CASCADE,verbose_name='Currency')
	address = models.CharField(max_length=300,verbose_name='Address',blank=True,null=True)
	status=models.IntegerField(choices=Address_Status,default=0,verbose_name='Status')

	def __str__(self):
		return self.address
	class Meta:
		verbose_name = 'UserWallet'
		db_table ='p2Gw2fGKotK7NcaN'


