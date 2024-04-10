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

from locations.models import Country,State,Cities

from django.utils import timezone


General_Status = (
					(0,'Active'),
					(1,'Inactive'),
					
	)

User_Role = (
		(0,'Admin'),
		(1,'SubAdmin'),
		(2,'Tradeusers')
	)
User_Status =(
		(0,'Inactive'),
		(1,'Active'),
		(2,'Deactive'),
		(3,'Cancelled')
	)

Gender = (

	(0,'Male'),
	(1,'Female'),
	)

Pattern_Status =(
  (0,'Not Updated'),
  (1,'Updated'),
  
 )

class AdminUser_Profile(models.Model):
	user = models.OneToOneField(User,related_name ='admin_user_profile',on_delete=models.CASCADE)
	gender = models.IntegerField(choices=Gender,verbose_name='Gender',blank=True,null=True)
	date_of_birth = models.DateField(help_text='Date of Birth in mm/dd/yyyy Format',blank=True,null=True)
	emailaddress = models.CharField(max_length=100,verbose_name="Email Address",blank=True,null=True)
	address1 = models.CharField(max_length=100,verbose_name='Contact Address1')
	address2 = models.CharField(max_length=100,verbose_name='Contact Address2',blank=True,null=True)
	city = models.CharField(max_length=30,verbose_name='City',blank=True,null=True)
	state = models.CharField(max_length=50,verbose_name='State',blank=True,null=True)
	country = models.ForeignKey(Country,related_name ='admin_user_country',on_delete=models.CASCADE,verbose_name='Country',blank=True,null=True)
	agree = models.BooleanField(default=False)
	postcode = models.CharField(max_length=10,verbose_name='Pin Code',blank=True,null=True)
	phone1 = models.CharField(max_length=13,verbose_name='Phone Number',blank=True,null=True)
	photo = models.ImageField(upload_to='tradeuserprofile',verbose_name='Profile Picture',blank=True,null=True)
	role = models.IntegerField(choices=User_Role,default=0,verbose_name='Role')
	pattern_code = models.IntegerField(verbose_name='Pattern Code',default=0)
	country_code = models.CharField(max_length=10,verbose_name='Country Code',blank=True,null=True)
	twofa = models.BooleanField(default=False)
	google_id = models.CharField(max_length=50,verbose_name='Google Id',blank=True,null=True)
	status = models.IntegerField(choices=User_Status,default=0,verbose_name = 'Status')
	pattern_status=models.IntegerField(choices=Pattern_Status,default=1,verbose_name = 'Pattern Status')
	def __str__(self):
		return "%s's profile" % self.user
	@property
	def image_name(self):
		return  os.path.basename(self.photo.path) if self.photo else ''
	
	class Meta:
		db_table='AYLkV0WRrgK0R9qM'
		verbose_name = "Admin Profile"
		verbose_name_plural ="Admin Profile's"
		indexes = [
		models.Index(fields=['gender','twofa','status'])

		]


class AdminUser_Activity(Auditable):
	user = models.ForeignKey(User,related_name ='admin_user_activity',on_delete=models.CASCADE)
	ip_address = models.GenericIPAddressField()
	activity=models.CharField(max_length=50,verbose_name='Activity',blank=True,null=True)
	browsername = models.CharField(max_length=50,verbose_name='Browser Name',blank=True,null=True)
	os=models.CharField(max_length=50,verbose_name='Operating System',blank=True,null=True)
	devices=models.CharField(max_length=50,verbose_name='Devices',blank=True,null=True)

	def __int__self(self):
		return id

	class Meta:
		verbose_name='AdminUser Activity'
		db_table = 'AWxn5AxwlScnvVij'


class AccessAttempt(models.Model):
	user = models.ForeignKey(User,related_name ='accessattempt',on_delete=models.CASCADE,blank=True,null=True)
	emailaddress = models.CharField(max_length=50,verbose_name='Email Address',blank=True,null=True)
	ip_address = models.GenericIPAddressField()
	activity=models.CharField(max_length=50,verbose_name='Activity',blank=True,null=True)
	browsername = models.CharField(max_length=50,verbose_name='Browser Name',blank=True,null=True)
	os=models.CharField(max_length=50,verbose_name='Operating System',blank=True,null=True)
	devices=models.CharField(max_length=50,verbose_name='Devices',blank=True,null=True)
	datetime = models.DateTimeField(default=timezone.now,verbose_name="DateTime")
	failedcount = models.IntegerField(verbose_name="Failed Logins")

	class Meta:
		verbose_name = "Access Attempt"
		db_table='AVyjW0gtKU25eYSY'
		indexes = [
		models.Index(fields=['user','failedcount','ip_address','datetime'])

		]

STATUS = (
	(0,'Active'),
	(1,'InActive')
)
SCHEME_TYPE=(
	(0,'Amount'),
	(1,'Weight')
)
class Scheme(models.Model):
	Scheme_name = models.CharField(max_length=250,blank=True,null=True,verbose_name="Scheme Name")
	Scheme_type = models.IntegerField(choices=SCHEME_TYPE,default=0,verbose_name="Scheme Type")
	Scheme_amount = models.CharField(max_length=250,blank=True,null=True,verbose_name="Scheme Amount")
	Scheme_number = models.CharField(max_length=250,blank=True,null=True,verbose_name="Scheme Number")
	Register_number = models.CharField(max_length=250,blank=True,null=True,verbose_name="Register Number")
	status = models.IntegerField(choices=STATUS,default=0,verbose_name='Status')
	Branch_id = models.CharField(max_length=250,blank=True,null=True,verbose_name="Branch Id")
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name ='Scheme'
		db_table='SCHzWkaJsitsYeR'


class Scheme_amount_master(models.Model):
	Scheme_id = models.CharField(max_length=250,blank=True,null=True,verbose_name="Scheme Id")
	Scheme_name = models.CharField(max_length=250,blank=True,null=True,verbose_name="Scheme Name")
	Scheme_amount = models.CharField(max_length=250,blank=True,null=True,verbose_name="Scheme Amount")
	user_count = models.CharField(max_length=250,blank=True,null=True,verbose_name="User Count")
	status = models.IntegerField(choices=STATUS,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name ='Scheme Amount Master'
		db_table='SCHAMTWkaJtsYeR'


class Gold_master(models.Model):
	Metal_id = models.CharField(max_length=250,blank=True,null=True,verbose_name="Metal Id")
	Metal_name = models.CharField(max_length=250,blank=True,null=True,verbose_name="Metal Name")
	Metal_amount = models.CharField(max_length=250,blank=True,null=True,verbose_name="Metal Amount")
	status = models.IntegerField(choices=STATUS,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name ='Gold Master'
		db_table='GOLjkghsiJtiuo'

class MenuModule(models.Model):
	module_code =models.CharField(max_length=20,verbose_name='Module Code')
	module_name = models.CharField(max_length=50,verbose_name='Module Name')
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)


	def __int__self(self):
		return id
	class Meta:
		verbose_name = 'MenuModules'
		db_table='21HbadiSPqTR4E0L'

class MenuPermission(Auditable):
	user_permissions = models.ForeignKey(User,related_name ='admin_user_menupermissions',on_delete=models.CASCADE)
	access_modules = models.ForeignKey(MenuModule,on_delete=models.CASCADE)
	Permission_Access =(
		(0,'NotAssign'),
		(1,'Write'),
		(2,'Read'),
	)
	access_permissions=models.IntegerField(choices=Permission_Access,verbose_name='Access Permissions',blank=True,null=True)
	ACCESS_STATUS = (
		(0,'Access'),
		(1,'Denied')
	)
	access_status=models.IntegerField(choices=ACCESS_STATUS,verbose_name='Access Status',blank=True,null=True)
	def __int__self(self):
		return id
	class Meta:
		verbose_name ='MenuPermissions'
		db_table='12s8VH6oGW3Zh7F0'



class SubMenuModule(models.Model):
	main_module_name = models.ForeignKey(MenuModule,related_name ='main_menu_module',on_delete=models.CASCADE)
	sub_module_name = models.CharField(max_length=50,verbose_name='Sub Module Name')
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)


	def __int__self(self):
		return "%s" % self.sub_module_name
	class Meta:
		verbose_name = 'SubMenuModules'
		db_table='31HbadiSPqTRSub'

class SubMenuPermission(Auditable):
	user_permissions = models.ForeignKey(User,related_name ='sub_user_menupermissions',on_delete=models.CASCADE)
	main_access_modules = models.ForeignKey(MenuPermission,related_name ='main_access_modules',on_delete=models.CASCADE)
	sub_menu_name = models.ForeignKey(SubMenuModule,related_name ='sub_menu_name',on_delete=models.CASCADE)
	Permission_Access =(
		(0,'NotAssign'),
		(1,'Write'),
		(2,'Read'),
	)
	access_permissions=models.IntegerField(choices=Permission_Access,verbose_name='Access Permissions',blank=True,null=True)
	ACCESS_STATUS = (
		(0,'Access'),
		(1,'Denied')
	)
	access_status=models.IntegerField(choices=ACCESS_STATUS,verbose_name='Access Status',blank=True,null=True)
	def __int__self(self):
		return id
	class Meta:
		verbose_name ='SubMenuPermissions'
		db_table='51s8VpermoGW3Zh7F0sub'