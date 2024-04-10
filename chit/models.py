from django.db import models
from django.core.validators import RegexValidator



# Create your models here.


General_Status = (
					(0,'Active'),
					(1,'Inactive'),					
	)

class User_Management(models.Model):
    user_name = models.CharField(max_length=250,blank=True,null=True,verbose_name="User Name")
    Email = models.EmailField(max_length=250, blank=True, null=True, verbose_name="Email")
    mobile_number = models.CharField(max_length=10,validators=[RegexValidator(regex=r'^\+?1?\d{9,10}$',message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")],blank=True,null=True,verbose_name="Mobile Number")
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now=True)

    

    class Meta:
        verbose_name ='User Management'
        db_table='USDQLUkJuU9TNt8m'


class otp_Registration(models.Model):
	user = models.ForeignKey(User_Management,related_name ='otp_registration',on_delete=models.CASCADE,blank=True,null=True)
	email_otp = models.IntegerField(verbose_name="Email Registration OTP",blank=True,null=True)
	phone_number_opt = models.IntegerField(verbose_name="Phone Number Registration OTP",blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=1,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "OTP Registration"
		db_table='OTPzTPzfNdmGTlER'
            

class MPin(models.Model):
	user = models.ForeignKey(User_Management,related_name ='MPin',on_delete=models.CASCADE,verbose_name='User')
	pin = models.IntegerField(verbose_name="User Individual Pin",blank=True,null=True)
	status =models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "M Pin"
		db_table = 'MPINSWITHkpbdzR'
