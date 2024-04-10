from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm,PasswordChangeForm

from django.forms import ModelChoiceField

from django.forms import widgets
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User,Group
from company.models import Company,Company_Settings
from trade_admin_auth.models import AdminUser_Profile, Gold_master,Scheme

from betterforms.multiform import MultiModelForm,MultiForm
from django.core.validators import MinValueValidator, MaxValueValidator
from collections import OrderedDict
from django.contrib.auth.forms import UserCreationForm

from trade_master.models import Blockip

from chit.views import encrypt_with_common_cipher




class Passwordreset(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']

class SetPasswordForm1(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput),
    new_password2 = forms.CharField(widget=forms.PasswordInput)
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        passowrd2 = self.cleaned_data.get('new_password2')
        if password1 and passowrd2:
            if len(passowrd2) < 8:
                raise forms.ValidationError(
                    self.error_messages['password_length'],
                    code='password_length',
                )
            if password1 != password2:
                raise forms.ValidationError(
                        self.error_messages['password_mismatch'],
                        code='password_mismatch'
                    )
        return passowrd2
    error_messages = {
    'password_length' : ("Password Must Have 8 Characters"),
    'password_mismatch' : ("Two Password Fieslds Does not match")
    }



class SetPasswordForm(forms.Form):
    
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password * "),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation * "),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2


class EditCompanyForm(forms.ModelForm):
    class Meta:
        model= Company
        
        fields=['name','email','phone1','company_logo','company_fav','copy_right','telegram','fb','twitter','instagram','linkedin','address1','city','Gst_number','pan_number']

        exclude=['created_on','modified_on','state','admin_redirect','country','postcode']

class EditCompanySettingsForm(forms.ModelForm):
    
    site_maintenance = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}),required = False)
    class Meta:
        model= Company_Settings
        
        fields=['site_maintenance_status','adminipaddress']

        exclude=['company_settings_name','site_maintenance']


class EditCompanyMultiForm(MultiModelForm):
    
    form_classes = {
        'form1': EditCompanyForm,
        'form2': EditCompanySettingsForm,
    }


class AdminUserAddForm(UserCreationForm):
    class Meta:
        model= User
        fields=['username','password1', 'password2',]
        exclude=['is_staff','first_name', 'last_name', 'email']

    


class AdminUserProfileAddform(forms.ModelForm):
    emailaddress = forms.CharField(required = True,label='Email ')
    pattern_code = forms.CharField(initial='',widget=forms.widgets.HiddenInput(),required=True)
    def clean_emailaddress(self):
        emailaddress = self.cleaned_data.get('emailaddress') 
        encrypt_username=encrypt_with_common_cipher(emailaddress)
        if AdminUser_Profile.objects.filter(emailaddress=encrypt_username).count() > 0:

            raise forms.ValidationError(u'This email address is already registered.')
        return emailaddress
    class Meta:
        model= AdminUser_Profile
        fields='__all__'
        exclude=['created_on','modified_on','user','state','role','address1',
        'address2','date_of_birth','referal_status','referal_code','refer_by_id','referal_user_by','status',
        'gender','phone1','photo','city','emailaddress','country','postcode','country_code','google_id','pattern_status'
        ]


class AdminUserAddMultiForm(MultiModelForm):
    form_classes = {
        'form1': AdminUserAddForm,
        'form2': AdminUserProfileAddform,
        
        }

class AdminUserEditsubForm(UserCreationForm):
    email = forms.CharField(required = True)
    
    

    class Meta:
        model= User
        fields=['username', 'email','password1', 'password2',]
        exclude=['is_staff','first_name', 'last_name', ]
class AdminSubadmineditform(forms.ModelForm):
  
    
    class Meta:
        model= AdminUser_Profile
        fields='__all__'
        exclude=['created_on','modified_on','user','state','role','address1',
        'address2','date_of_birth','referal_status','referal_code','refer_by_id','referal_user_by','status',
        'gender','phone1','photo','city','country','postcode','country_code','google_id'
        ]

class AdminUserEditSubadminMultiForm(MultiModelForm):
    form_classes = {
        'form1': AdminUserEditsubForm,
        'form2': AdminSubadmineditform,
        
        }

class AdminUserProfileeditform(forms.ModelForm):
  
    
    class Meta:
        model= AdminUser_Profile
        fields=['emailaddress','phone1','photo']
        exclude=['user_id','created_on','modified_on','user','state','role',
        'address2','date_of_birth','pattern_code'
        ,'gender','address1','city','country','postcode','list_country','country_code','authy_id','google_id'
        ]


class AdminUserEditForm(forms.ModelForm):
    email = forms.CharField(required = True)
    
    class Meta:
        model= User
        fields=['email','username']
        exclude=['is_staff','first_name', 'last_name','password1', 'password2',]

class AdminUserEditMultiForm(MultiModelForm):
    form_classes = {
        'form1': AdminUserEditForm,
        'form2':AdminUserProfileeditform
        }
class SubAdminUserProfileeditform(forms.ModelForm): 
    class Meta:
        model= AdminUser_Profile
        fields=['emailaddress','user']
        exclude=['photo','created_on','modified_on','user','state','role',
        'address2','date_of_birth','pattern_code'
        ,'gender','address1','city','country','postcode','list_country','country_code','authy_id','google_id'
        ]


class ChangePatternForm(forms.ModelForm):

    pattern_code = forms.CharField(initial=0,widget=forms.widgets.HiddenInput())
    class Meta:
        model= AdminUser_Profile
        fields='__all__'
        exclude=['created_on','modified_on','user','state','role',
        'address2','date_of_birth','refer_id','refer_user_id','refer_by_id','activation_date',
        'address1','city','country','postcode','phone1','gender','photo','country_code','authy_id','google_id'
        ]

class GoogleTokenVerificationForm(forms.Form):
    token = forms.CharField(required=True,label='TwoFA Code')

class BlockipForm(forms.ModelForm):
    
    class Meta:
        model = Blockip
        fields = ['ip_address','ip_option','ip_level','status']
        exclude = ['created_on','modified_on']


class scheme_master_Form(forms.ModelForm):
    
    class Meta:
        model = Scheme
        fields = ['Scheme_name','Scheme_type']
        exclude = ['created_on','modified_on','Scheme_amount','Scheme_number','Register_number','status','Branch_id']
