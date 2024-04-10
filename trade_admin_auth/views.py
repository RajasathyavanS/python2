
from django.shortcuts import render
from django.shortcuts import render,get_list_or_404, get_object_or_404

from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views.generic import TemplateView,View

from django.http.response import HttpResponseRedirect
from django.http import HttpResponse,Http404
from django.urls import reverse
from django.urls import reverse_lazy
from django.template.context_processors import csrf
from django.shortcuts import redirect
from django.http import JsonResponse

from datetime import date,timedelta
import datetime
import string
import random

from django.db.models import Q,F,Func,Value
from django.db.models import Count, Min,Max, Sum, Avg,DecimalField,DateTimeField,CharField
from django.db.models.expressions import RawSQL
from django.db.models.functions import Cast,TruncSecond,ExtractSecond


from django.db import transaction

from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required,user_passes_test
from django.core.exceptions import PermissionDenied
from auditable.views import AuditableMixin

from Crypto.Cipher import AES
import base64
import math
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.http.response import HttpResponseRedirect

from django_ajax.decorators import ajax


from django_tables2 import RequestConfig
from django_tables2 import RequestConfig
from crispy_forms.layout import Submit,ButtonHolder,Reset


from trade_admin_auth.mixins import check_group
from trade_admin_auth.mixins import SubAdminRequiredMixin,CheckIpaddressAdminRequiredMixin
from trade_admin_auth.mixins import get_client_ip,get_browser_type,get_browser_os_type,get_browser_device_type,allow_by_ip,check_adminip
from trade_admin_auth.mixins import ManageUserAdminRequiredMixin,ManageBlockipAdminRequiredMixin,BlockIpaddressAdminRequiredMixin
from operator import itemgetter


from company.models import Company,Company_Settings
from trade_admin_auth.models import AdminUser_Profile,AdminUser_Activity,AccessAttempt, Gold_master, MenuModule, MenuPermission,Scheme, Scheme_amount_master, SubMenuModule, SubMenuPermission
from trade_admin_auth.serializers import gold_amount_Serializer, scheme_Serializer, scheme_amount_Serializer


from trade_admin_auth.tables import AdminActivityTable,DeactivateUserTable, SubAdminTable
from trade_admin_auth.tables import AdminActivityTableFilter,AdminActivitySearch_Form
from trade_admin_auth.tables import DashboardAdminActivityTable,BlockIPTable
from django.contrib.auth.forms import PasswordChangeForm

from trade_master.models import Contactus,Cms_StaticContent,Blockip,EmailTemplate,Roadmap,Faq

#from trade_auth.models import UserAddress,UserWallet
#from trade_auctions.models import Auctions,Bids,WinnerAuctions
#from trade_admin_auth.tables import UserAddressTable
#from support.models import SupportCategory,SupportTicket,SupportTicketDetails
from trade_admin_auth.forms import EditCompanyForm,EditCompanySettingsForm,EditCompanyMultiForm, SubAdminUserProfileeditform
from trade_admin_auth.forms import AdminUserAddForm,AdminUserAddMultiForm
from trade_admin_auth.forms import AdminUserEditForm,AdminUserEditMultiForm,AdminUserProfileeditform,ChangePatternForm,AdminUserEditSubadminMultiForm
from trade_admin_auth.forms import GoogleTokenVerificationForm,BlockipForm,scheme_master_Form
from trade_admin_auth.forms import Passwordreset,SetPasswordForm,PasswordChangeForm
import requests
import uuid
import pyotp
import json


from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from django.utils.decorators import method_decorator

from decimal import Decimal
import os
import decimal

from trade_currency.models import TradeCurrency,TradePairs

def allow_by_ip(view_func):
    def authorize(request, *args, **kwargs):
        user_ip = get_client_ip(request)
        allowedIps = Blockip.objects.filter(Q(status=0) & Q(ip_level="Admin"))
        for ip in allowedIps:
            if ip.ip_address == user_ip:
                return HttpResponseRedirect("/tradeadmin/adminblockip404/")
        return view_func(request, *args, **kwargs)
    return authorize

def Page403View(request):
	return render(request,'trade_admin_auth/403page.html',status=403)

def Page404View(request):
	return render(request,'trade_admin_auth/404page.html',status=404)

def Page500View(request):
	return render(request,'trade_admin_auth/500page.html',status=500)


def IPBlock404View(request):
  try:
    companyqs = Company.objects.get(id=1)
    companyname= companyqs.name
    companyipaddress = companyqs.company_settings.adminipaddress
  except Company.DoesNotExist:
    companyqs = 'HotBitDeal Auction'
    companyname = 'HotBitDeal Auction'
    companyipaddress = ''
  user_ip = get_client_ip(request)
  if companyipaddress is None or companyipaddress == '':
    return HttpResponseRedirect("/W8n9cQU3MAh1mjhT/")
  if companyipaddress == user_ip:
    return HttpResponseRedirect("/W8n9cQU3MAh1mjhT/")
  if companyipaddress is not None and companyipaddress != '':
    if companyipaddress != user_ip:
      pass
  return render(request,'trade_admin_auth/ipblock404.html',status=404)


def adminblockip404(request):
    user_ip = get_client_ip(request)
    allowedIps = Blockip.objects.filter(Q(status=1) & Q(ip_level="Admin"))
    for ip in allowedIps:
        if ip.ip_address == user_ip:
            return HttpResponseRedirect("/W8n9cQU3MAh1mjhT/")
    return render(request,"trade_admin_auth/ipblock.html")


def blockipadmin(request):
    attempt = check_attempts(request)
    if attempt == 2:
        return HttpResponseRedirect("/W8n9cQU3MAh1mjhT/")
    elif attempt == 1:
        return render(request,"trade_admin_auth/ipblock.html")


def check_attempts(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    attempt = AccessAttempt.objects.filter(ip_address=ip)
    access_count = len(attempt)
    a = ''
    if access_count >= 5 :
        a = 1
    else:
        a = 2
    return a


def get_email_template(request,email_temp_id):
    email_template = EmailTemplate.objects.get(id = email_temp_id)
    if email_template:
        email_template_qs =email_template
    else:
        email_template_qs = ''
    return email_template_qs



def get_common_cipher():
    return AES.new(settings.COMMON_ENCRYPTION_KEY,
                   AES.MODE_CBC,
                   settings.COMMON_16_BYTE_IV_FOR_AES)

def encrypt_with_common_cipher(cleartext):
    common_cipher = get_common_cipher() 
    cleartext_length = len(cleartext)
    nearest_multiple_of_16 = 16 * math.ceil(cleartext_length/16)
    padded_cleartext = cleartext.rjust(nearest_multiple_of_16)
    raw_ciphertext = common_cipher.encrypt(padded_cleartext.encode("utf8"))
    return base64.b64encode(raw_ciphertext).decode('utf-8')

def decrypt_with_common_cipher(ciphertext):
    common_cipher = get_common_cipher()
    raw_ciphertext = base64.urlsafe_b64decode(ciphertext)
    decrypted_message_with_padding = common_cipher.decrypt(raw_ciphertext)
    return decrypted_message_with_padding.decode('utf-8').strip()

@allow_by_ip
@check_adminip('checkadminip')
def adminlogin(request):
    context ={}
    context.update(csrf(request))
    attempt = check_attempts(request)
    if attempt == 1:
        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
    elif attempt == 2:
        return render(request, 'trade_admin_auth/login.html', context)

@allow_by_ip
def adminlogin_auth(request):
    attempt = check_attempts(request)
    if attempt == 1:
        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
    elif attempt == 2:
        get_username_enc = request.POST.get('username', '')
        get_username = encrypt_with_common_cipher(get_username_enc)
        get_password = request.POST.get('password', '')
        get_patterncode = request.POST.get('pattern_code', '')
        try:
            if '@' in get_username_enc:
              try:
                userprofile= AdminUser_Profile.objects.get(emailaddress =get_username)
                if userprofile:
                  useremail = userprofile.user.username
                  username = User.objects.get(username=useremail).username
                  
                else:
                  username =''
              except AdminUser_Profile.DoesNotExist:
                userprofile =''
                username =''
            else:
                username = ''
            user = auth.authenticate(request=request,username=username,
                                     password=get_password)

        except User.DoesNotExist:
            user = None
        if user is not None:
            user_id = user.id
            get_userprofile = AdminUser_Profile.objects.get(user_id=user_id)
            user_pattern = get_userprofile.pattern_code
        else:
            user_pattern = ''
            
        if user is not None:
          
            if user_pattern is not None and user_pattern == int(get_patterncode):
                if user is not None and user.is_active:
                    userid = user.id
                    userprofile = AdminUser_Profile.objects.get(user = userid)
                    userprofile2fa = userprofile.twofa
                    if userprofile2fa == False:
                      auth.login(request, user)
                      next_URL = '/tradeadmin/dashboard/'
                      
                      admin_activity_history(request, user.id,
                            typelogin='Login')
                      return HttpResponseRedirect(next_URL)
                    elif userprofile2fa == True:
                      next_URL= '/tradeadmin/twofaadmin/'+str(userid)+'/'
                      return HttpResponseRedirect(next_URL)
                    
                else:
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[0]
                    else:
                        ip = request.META.get('REMOTE_ADDR')
                    attempt = AccessAttempt.objects.filter(ip_address=ip)
                    access_count = len(attempt)
                    if access_count >= 5 :
                        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
                    else:
                        tradeadmin_attempt_history(request,get_username_enc ,typelogin='Invalid Admin Login')
                        messages.add_message(request, messages.ERROR, 'Login Details are invalid')
                        return HttpResponseRedirect('/W8n9cQU3MAh1mjhT/')
            else:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                attempt = AccessAttempt.objects.filter(ip_address=ip)
                access_count = len(attempt)
                if access_count >= 5 :
                    return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
                else:
                    tradeadmin_attempt_history(request,get_username_enc ,typelogin='Invalid Admin Login')
                    messages.add_message(request, messages.ERROR, 'Login Details are invalid')
                    return HttpResponseRedirect('/W8n9cQU3MAh1mjhT/')
        else:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            attempt = AccessAttempt.objects.filter(ip_address=ip)
            access_count = len(attempt)
            if access_count >= 5 :
                return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
            else:
                tradeadmin_attempt_history(request,get_username_enc ,typelogin='Invalid Admin Login')
                messages.add_message(request, messages.ERROR, 'Login Details are invalid')
                return HttpResponseRedirect('/W8n9cQU3MAh1mjhT/')


def tradeadmin_attempt_history(request,get_email,typelogin):
    try:
        get_user = User.objects.get(email=get_email)
        if get_user:
            create_admin_login = AccessAttempt.objects.create(
                user = get_user,
                emailaddress = get_email,
                ip_address=get_client_ip(request),
                activity=typelogin,
                browsername=get_browser_type(request),
                os=get_browser_os_type(request),
                devices=get_browser_device_type(request),
                datetime=datetime.datetime.now(),
                failedcount = 1
              )  
    except:
        create_admin_login = AccessAttempt.objects.create(
            emailaddress = get_email,
            ip_address=get_client_ip(request),
            activity=typelogin,
            browsername=get_browser_type(request),
            os=get_browser_os_type(request),
            devices=get_browser_device_type(request),
            datetime=datetime.datetime.now(),
            failedcount = 1
          )
    return  True


def admintwofa(request,uid):
    context={}
    context = {
    'Title':'Two Factor Authenticator',
    'keywords':'Enable Google Authenticator,QR Code',
    'content':'Enable Google Authenticator  for additional security for user.',
    }
    if request.method == 'POST':
        form = GoogleTokenVerificationForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(pk=uid)
                user_id = user.id
                get_userprofile = AdminUser_Profile.objects.get(user = user_id)
            except User.DoesNotExist:
                user = None
                get_userprofile = None
            if user is not None and get_userprofile is not None:
                secertkey = get_userprofile.google_id
                authtoken = pyotp.TOTP(secertkey)
                verification = authtoken.now()
                token = request.POST['token']
                if token == verification:
                    auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                    admin_activity_history(request,user_id,typelogin='Login')
                    messages.add_message(request, messages.SUCCESS, 'two factor authentication login successfully.')
                    return HttpResponseRedirect('/tradeadmin/dashboard/')
                else:
                    messages.add_message(request, messages.ERROR,'Invalid 2FA Code')
                    return HttpResponseRedirect('/tradeadmin/twofaadmin/'+str(user_id)+'/')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid user!')
                return HttpResponseRedirect('/tradeadmin/twofaadmin/'+str(user_id)+'/')
    else:
        form = GoogleTokenVerificationForm()
    return render(request, 'trade_admin_auth/twofalogin.html', {'form': form})



def log_out(request):
    admin_activity_history(request,request.user.id,typelogin='Logout')
    auth.logout(request)
    return HttpResponseRedirect('/W8n9cQU3MAh1mjhT/')

def user_date_charts(request):
    today = datetime.datetime.today()
    long_ago = today + timedelta(days=-7)
    d=date.today()-timedelta(days=6)
    adminactivity_list = []
    json_result=''
    adminactivity = AdminUser_Activity.objects.filter(Q(activity='Login') & Q(user__admin_user_profile__role=2) & Q(created_on__gte=d)).extra({'date_created':"date(modified_on)"}).values('date_created').order_by('modified_on__date').annotate(tot_deposit_amt=Count('id'))
    
    if adminactivity:
      for adminitem in adminactivity:
        adminday = adminitem['date_created']
        admindayname = adminday.strftime("%a")
        adminactivity_sub_list =[]
        admincount= int(adminitem['tot_deposit_amt'])
        adminactivity_sub_list.append(admindayname)
        adminactivity_sub_list.append(admincount)
        adminactivity_list.append(adminactivity_sub_list)
      json_result = adminactivity_list
    else:
      json_result ='0'  
    return json_result



def admin_activity_history(request,user_id,typelogin):
    get_user = User.objects.get(id=user_id)
    if get_user:
          create_admin_login = AdminUser_Activity.objects.create(
            user_id=user_id,
            ip_address=get_client_ip(request),
            activity=typelogin,
            browsername=get_browser_type(request),
            os=get_browser_os_type(request),
            devices=get_browser_device_type(request),
            created_on=datetime.datetime.now(),
            created_by_id = get_user.id,
            modified_by_id = get_user.id

          )   

    return  True


@allow_by_ip
@check_adminip('checkadminip')
def dashboard(request):
    attempt = check_attempts(request)
    if attempt == 1:
        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
    elif attempt == 2:
        context={}
        context['Title'] = 'Dashboard'
        adminactivity_qs = AdminUser_Activity.objects.filter(user__admin_user_profile__role=0).order_by('-id')[:10]
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = DashboardAdminActivityTable(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['dashboardshow'] = 'Yes'
        auction_count=Gold_master.objects.all().last()
        if auction_count == None:
          gold_rate=0
        else:
          gold_rate = auction_count.Metal_amount
        context['auction_count']=gold_rate
        return render(request,"trade_admin_auth/dashboard.html",context)


def randomString(stringLength=16):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def adminforgotpassword(request):
  attempt = check_attempts(request)
  if attempt == 1:
    return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
  elif attempt == 2:
    context ={}
    if  request.method == 'POST':
        form = Passwordreset(request.POST)
        if form.is_valid():
          get_email = request.POST.get('email','')
          try:
            companyqs = Company.objects.get(id=1)
            copyright= companyqs.copy_right
            comp_logo = companyqs.company_logo
          except:
            companyqs = ''
            copyright = ''
            comp_logo=''
          try:
            get_user = User.objects.get(Q(email = get_email) & Q(is_superuser=True))
            checkemail = get_user.email
            checkuser_id = get_user
          except:
            get_user = None
            checkemail = None
            checkuser_id = None
          if checkemail is not None:

            emailtemplate = get_email_template(request,1)
            text_file = open("trade_master/templates/emailtemplate/forgot_mail.html", "w")
            text_file.write(emailtemplate.content)
            text_file.close()
            email_subject = emailtemplate.Subject
            to_email = checkemail
            from_email_get = settings.EMAIL_USER
            from_email =decrypt_with_common_cipher(from_email_get)
            from_email =decrypt_with_common_cipher(from_email_get)
            hostuser = decrypt_with_common_cipher(settings.EMAIL_USER_ENC)
            hostpassword = decrypt_with_common_cipher(settings.EMAIL_PASSWORD_ENC)
            settings.EMAIL_HOST_USER = hostuser
            settings.EMAIL_HOST_PASSWORD = hostpassword
            
            data= {
              'username':checkuser_id,
              'company_logo':comp_logo,
              'copyright':copyright,
              'domain':get_current_site(request),
              'uid':urlsafe_base64_encode(force_bytes(get_user.pk)),
              'token':default_token_generator.make_token(get_user),
              'protocol': 'http',
              }
            text_content = 'This is an important message.'
            htmly = get_template('emailtemplate/forgot_mail.html')
            html_content = htmly.render(data)
            msg = EmailMultiAlternatives(email_subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.add_message(request, messages.SUCCESS, 'Your Password Link sent to  your EmailId.') 
            return HttpResponseRedirect('/W8n9cQU3MAh1mjhT/')
          else:
            messages.add_message(request, messages.ERROR, 'Invalid EmailID')  
            return HttpResponseRedirect(reverse('trade_admin_auth:adminforgotpassword'))
        else:
          messages.add_message(request,messages.INFO,'Error Occured.')
    else:
        form = Passwordreset()
    return render(request,"trade_admin_auth/adminforgot.html",context)    


def Admin_passwordresetconfirm(request, uidb64, token):
    username = request.user.username
    if username != None and username !='':
      return HttpResponseRedirect('/tradeadmin/dashboard/')
    else:
      if request.method == 'POST':
          form = SetPasswordForm(request.POST)
          if form.is_valid():
            UserModel = get_user_model()
            assert uidb64 is not None and token is not None
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = UserModel._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user, token):
                try:
                    new_password = form.cleaned_data['new_password2']
                    user.set_password(new_password)
                    user.is_active =True
                    user.save()
                    get_userprofile = AdminUser_Profile.objects.get(user = user.id)
                    get_userprofile.status = 1
                    get_userprofile.save()
                    messages.add_message(request,messages.SUCCESS,'Your Password Reset Successfully Now You Login ')
                    return HttpResponseRedirect("/W8n9cQU3MAh1mjhT/")
                except KeyError:
                    messages.add_message(messages.ERROR,'Two Password Fields Did not match')
            else:
                messages.add_message(request, messages.ERROR, 'Reset link already used !!')
                next_URL = '/W8n9cQU3MAh1mjhT/'
                return HttpResponseRedirect(next_URL)
          else:
              messages.add_message(request,messages.ERROR,form.errors)
              next_URL = '/W8n9cQU3MAh1mjhT/'
              return HttpResponseRedirect(next_URL)
      else:
          form = SetPasswordForm()
          UserModel = get_user_model()
          assert uidb64 is not None and token is not None
          try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel._default_manager.get(pk=uid)
          except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
          if user is not None and default_token_generator.check_token(user, token):
            pass
          else:
            messages.add_message(request, messages.ERROR, 'Reset link already used !!')
            return HttpResponseRedirect('/W8n9cQU3MAh1mjhT/')
    return render(request,"trade_admin_auth/adminpasswordconfirm.html",{'form':form})

@allow_by_ip
def adminforgotpattern(request):
  context ={}
  if  request.method == 'POST':
    get_email = request.POST.get('email','')
    try:
      companyqs = Company.objects.get(id=1)
      copyright= companyqs.copy_right
      comp_logo = companyqs.company_logo
    except:
      companyqs = ''
      copyright = ''
      comp_logo=''
    try:
      get_user = User.objects.get(Q(email = get_email) & Q(is_superuser=True))
      checkemail = get_user.email
      checkuser_id = get_user
    except:
      get_user = None
      checkemail = None
      checkuser_id = None
    if checkemail is not None:
      profile = AdminUser_Profile.objects.get(user=get_user)
      profile.pattern_status = 0
      profile.save()
      emailtemplate = get_email_template(request,2)
      text_file = open("trade_master/templates/emailtemplate/forgotpattern_mail.html", "w")
      text_file.write(emailtemplate.content)
      text_file.close()
      email_subject = emailtemplate.Subject
      to_email = checkemail
      from_email_get = settings.EMAIL_USER
      from_email =decrypt_with_common_cipher(from_email_get)
      from_email =decrypt_with_common_cipher(from_email_get)
      hostuser = decrypt_with_common_cipher(settings.EMAIL_USER_ENC)
      hostpassword = decrypt_with_common_cipher(settings.EMAIL_PASSWORD_ENC)
      settings.EMAIL_HOST_USER = hostuser
      settings.EMAIL_HOST_PASSWORD = hostpassword
      
      data= {
        'username':checkuser_id,
        'company_logo':comp_logo,
        'copyright':copyright,
        'domain':get_current_site(request),
        'protocol':'http',
        'userid':get_user.id,
        'uid':urlsafe_base64_encode(force_bytes(get_user.pk)),
        'token':default_token_generator.make_token(get_user),
        }
      text_content = 'This is an important message.'
      htmly = get_template('emailtemplate/forgotpattern_mail.html')
      html_content = htmly.render(data)
      msg = EmailMultiAlternatives(email_subject, text_content, from_email, [to_email])
      msg.attach_alternative(html_content, "text/html")
      msg.send()
      messages.add_message(request, messages.SUCCESS, 'Pattern Reset Link Send To Your Email') 
      return HttpResponseRedirect('/W8n9cQU3MAh1mjhT/')
    else:
      messages.add_message(request, messages.ERROR, 'Invalid EmailID')  
      return HttpResponseRedirect(reverse('trade_admin_auth:adminforgotpattern'))
  else:
    return render(request,"trade_admin_auth/adminforgotpattern.html",context)    

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()


def Adminpatternupdate(request, uidb64, token):
  username = request.user.username
  if username != None and username !='':
    return HttpResponseRedirect('/tradeadmin/dashboard/')
  else:
    if request.method == 'POST':
        UserModel = get_user_model()
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        profile = AdminUser_Profile.objects.get(user=user)
        patternstatus = profile.pattern_status
        if user is not None and patternstatus == 0:
            patrn_upt = AdminUser_Profile.objects.get(user=user)
            ptn_id=user.id
            get_pattern_code = int(request.POST['pattern_code'])
            get_confirmpattern = int(request.POST['confirmpattern_code'])
            patterncode = get_pattern_code
            confirmpattern = get_confirmpattern
            if patterncode == confirmpattern:
              update_patterncode = AdminUser_Profile.objects.get(id = patrn_upt.id)
              update_patterncode.pattern_code = patterncode
              update_patterncode.pattern_status = 1
              update_patterncode.save()
              messages.add_message(request,messages.SUCCESS,'Pattern Updated Success')
              return HttpResponseRedirect("/W8n9cQU3MAh1mjhT/")
            else:
              messages.add_message(request, messages.ERROR, 'Confirm pattern is mismatch')
        else:
            messages.add_message(request, messages.ERROR, 'Reset link already used !!')
            next_URL = '/W8n9cQU3MAh1mjhT/'
            return HttpResponseRedirect(next_URL)
    else:
        UserModel = get_user_model()
        assert uidb64 is not None and token is not None
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        profile = AdminUser_Profile.objects.get(user=user)
        patternstatus = profile.pattern_status
        if user is not None and patternstatus == 0:
            pass
        else:
            messages.add_message(request, messages.ERROR, 'Reset link already used !!')
            return HttpResponseRedirect('/W8n9cQU3MAh1mjhT/')
  return render(request,'trade_admin_auth/forgotpatternconfirm.html')



class EditCompanySetting(CheckIpaddressAdminRequiredMixin,UpdateView):
    permission_required = ('trade_perms.Trade_Admin')
    
    model=Company
    form_class = EditCompanyMultiForm
    template_name = 'trade_admin_auth/settings.html'

    def get_context_data(self, **kwargs):
       context = super(EditCompanySetting, self).get_context_data(**kwargs)
       
       context['Title']='General Settings'
       return context
    def get_form_kwargs(self):
      
          kwargs = super(EditCompanySetting, self).get_form_kwargs()
          kwargs.update(instance={
              'form1': self.object,
              'form2': self.object.company_settings,
          })
          return kwargs
        

    def get_success_url(self, **kwargs):
        p_key = int(self.kwargs['pk'])
        messages.add_message(self.request, messages.SUCCESS, 'Setting Updated Successfully.')
        return '{}'.format(reverse('trade_admin_auth:general_settings', kwargs={'pk': p_key}))
      

@allow_by_ip
@check_adminip('checkadminip')
def editprofilesetting(request,user_id):
    attempt = check_attempts(request)
    if attempt == 1:
        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
    elif attempt == 2:
        context={}
        user= User.objects.get(id=user_id)
        usermail = user.email
        userprofile= AdminUser_Profile.objects.get(user=user.id)
        user_profile_id = userprofile.id
        user_decrypt_emailaddress =userprofile.emailaddress  
        decrypt_user_emailaddress=decrypt_with_common_cipher(user_decrypt_emailaddress)
        phoneno = userprofile.phone1
        profilepic = userprofile.photo
        if request.method == 'POST':
           profile_form = AdminUserProfileeditform(request.POST,request.FILES,instance=userprofile)
           getemail = request.POST['email']

           if getemail and User.objects.filter(Q(email=getemail) & Q(is_superuser=False)).count() > 0:
               messages.add_message(request, messages.ERROR, "This Email Address Already Registered")
               return HttpResponseRedirect('/tradeadmin/profile_settings/'+str(user_id)+'/')
           else:
               if profile_form.is_valid():
                 getusername = request.POST['username']
                 userupdateform = User.objects.filter(id=user_id).update(email = getemail , username = getusername)
                 get_emailaddress = getemail
                 profile_form.instance.created_by_id = request.user.id
                 profile_form.instance.modified_by_id = request.user.id
                 profile_form.save()
                 if get_emailaddress != "":
                    encrypt_useremail=encrypt_with_common_cipher(get_emailaddress)
                    update_emailaddress = AdminUser_Profile.objects.get(id = user_profile_id)
                    update_emailaddress.emailaddress = encrypt_useremail
                    update_emailaddress.save()
                   
                 else:
                    messages.add_message(request, messages.ERROR, 'Email address must required.')
                    return HttpResponseRedirect('/tradeadmin/profile_settings/'+str(user_id)+'/')
                 messages.add_message(request, messages.SUCCESS, 'Admin Profile updated Successfully.')
                 return HttpResponseRedirect('/tradeadmin/profile_settings/'+str(user_id)+'/')
               else:
                messages.add_message(request, messages.ERROR, user_form.errors)
                return HttpResponseRedirect('/tradeadmin/profile_settings/'+str(user_id)+'/')
        else:
            context={
                'Title':'Profile Setting',
                'decrypt_user_emailaddress':decrypt_user_emailaddress,
                'phoneno':phoneno,
                'profilepic':profilepic,
                'usermail':usermail
              }
        return render(request,'trade_admin_auth/profile.html', context)

class ChangePasswordView(PasswordChangeView):
  
    template_name = 'trade_admin_auth/changepassword.html'
    form_class = PasswordChangeForm
   
    def get_context_data(self, **kwargs):
       context = super(ChangePasswordView, self).get_context_data(**kwargs)
       context['Title']='Change Password'
       return context
   
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'Change password updated Successfully.')
        return '{}'.format(reverse('trade_admin_auth:change_password'))

class ChangePatternView(UpdateView):
    model= AdminUser_Profile
    template_name = 'trade_admin_auth/changepattern.html'
    form_class = ChangePatternForm
   
    def get_context_data(self, **kwargs):
       context = super(ChangePatternView, self).get_context_data(**kwargs)
       context['Title']='Change Pattern'
       return context
    @transaction.atomic
    def form_valid(self, form):
        formsave=form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Change pattern updated Successfully.')
        return HttpResponseRedirect(reverse('trade_admin_auth:patternchange',kwargs={'pk': formsave.id}))
    

def change_pattern_view(request,user_id):
    context={}
    user= User.objects.get(id=user_id)
    user_profile_id = user.admin_user_profile.id
    user_profile_pattern = user.admin_user_profile.pattern_code
  
    if request.method == 'POST':
       pattern_code = int(request.POST['pattern_code'])
       oldpattern = int(request.POST['old_pattern_code'])
       confirmpattern = int(request.POST['confirmpattern_code'])

       if oldpattern != "" and oldpattern == user_profile_pattern:
        if oldpattern !="" and confirmpattern != "" and pattern_code != "":
          if pattern_code == confirmpattern:
      
           if pattern_code != "":
              update_patterncode = AdminUser_Profile.objects.get(id = user_profile_id)
              update_patterncode.pattern_code = pattern_code
              update_patterncode.save()
              messages.add_message(request, messages.SUCCESS, 'Change pattern updated Successfully.')
           else:
              messages.add_message(request, messages.ERROR, 'New pattern must required.')
              return HttpResponseRedirect('/tradeadmin/patternchange/'+str(user_id)+'/')
         
          else:
            messages.add_message(request, messages.ERROR, 'Confirm pattern is mismatch')
            return HttpResponseRedirect('/tradeadmin/patternchange/'+str(user_id)+'/')
        else:
          messages.add_message(request, messages.ERROR, 'Pattern Code must required')
          return HttpResponseRedirect('/tradeadmin/patternchange/'+str(user_id)+'/')
       else:
        messages.add_message(request, messages.ERROR, 'Old pattern is mismatch')
        return HttpResponseRedirect('/tradeadmin/patternchange/'+str(user_id)+'/')
       
       return HttpResponseRedirect('/tradeadmin/patternchange/'+str(user_id)+'/')
    else:
          
        
        context={
            'Title':'Change Pattern',
            'patterncode':user_profile_pattern,
           }
        
    return render(request,'trade_admin_auth/changepattern.html', context)

def admintwofaupdate(request):
    form = GoogleTokenVerificationForm()
    if request.method == 'POST':
        form = GoogleTokenVerificationForm(request.POST)
        if form.is_valid():
            token = request.POST['token']
            secertkey = request.POST['secertkey']
            authtoken = pyotp.TOTP(secertkey)
            verification = authtoken.now()
            msg=''
            if token == verification:
                uid =request.user.id
                try:
                    user = User.objects.get(pk=uid)
                    user_id = user.id
                    get_userprofile = AdminUser_Profile.objects.get(user = user_id)

                except User.DoesNotExist:
                    user = None
                    get_userprofile = None
                if user is not None and get_userprofile is not None:
                    if get_userprofile.twofa == False:
                        get_userprofile.twofa = True
                        get_userprofile.google_id = secertkey
                        get_userprofile.save()
                        msg='two factor authentication enabled successfully.'
                    elif get_userprofile.twofa == True:
                        get_userprofile.twofa = False
                        get_userprofile.google_id = '' 
                        get_userprofile.save()
                        msg='two factor authentication disabled successfully.'

                    messages.add_message(request, messages.SUCCESS, msg)
                    return HttpResponseRedirect('/tradeadmin/admin2fa/')
                else:
                   messages.add_message(request, messages.ERROR, 'Already status updated.')
                   return HttpResponseRedirect('/tradeadmin/admin2fa/')
            else:
                messages.add_message(request, messages.ERROR,'Invalid 2FA Code')
                return HttpResponseRedirect('/tradeadmin/admin2fa/')
        else:
           messages.add_message(request, messages.ERROR,form.errors)
           return HttpResponseRedirect('/tradeadmin/admin2fa/') 
    else:
        try:
          get_userprofile = AdminUser_Profile.objects.get(user = request.user.id)
        except AdminUser_Profile.DoesNotExist:
         get_userprofile  = ''
        secertkey =''
        if get_userprofile.google_id != None and get_userprofile.google_id !='':
          secertkey = get_userprofile.google_id
        else:
          secertkey = pyotp.random_base32()

        pytop =pyotp.totp.TOTP(secertkey).provisioning_uri(name=request.user.email, issuer_name='HBD Auction Admin 2FA')
        verification = pyotp.TOTP(secertkey)
        authtoken = verification.now()
        usertwofastatus = get_userprofile.twofa
        usersecertkey = ''
        if usertwofastatus == True:
          usersecertkey = get_userprofile.google_id
        else:
          usersecertkey = secertkey

        context ={
          'Title':'Two Factor Authentication',
          'userpytop':pytop,
          'secertkey':usersecertkey,
          'get_userprofile':get_userprofile,
          'form5':GoogleTokenVerificationForm()

        }
    return render(request,'trade_admin_auth/enable2fa.html', context)


class ListAdminactivity(SubAdminRequiredMixin,ListView):
    model = AdminUser_Activity
    template_name = 'trade_admin_auth/subadmin_activity_list.html'
    def get_queryset(self, **kwargs):
      return AdminUser_Activity.objects.filter(Q(user__admin_user_profile__role=1) | Q(user__admin_user_profile__role=0)).order_by('-id')
    def get_context_data(self,**kwargs):
        context=super(ListAdminactivity, self).get_context_data(**kwargs)
        context['Title'] = 'Admin Login History'
        tradeuser_qs = AdminUser_Activity.objects.filter(Q(user__admin_user_profile__role=1) | Q(user__admin_user_profile__role=0)).order_by('-id')
        filter = AdminActivityTableFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = AdminActivitySearch_Form()
        filter.form.helper.add_input(Submit('submit', 'Search',css_class="btn btn-default"))
        filter.form.helper.add_input(Reset('Reset Search','Reset Search',css_class="btn btn-default",css_id='reset-search'))
        contenttable = AdminActivityTable(filter.qs)
        context['tradeuser_qs'] =tradeuser_qs
        context['table'] = contenttable
        RequestConfig(self.request, paginate={'per_page': 15}).configure(contenttable)
        context['filter'] = filter
        context['Reset_url'] = 'trade_admin_auth:subadminactivity'
        context['activecls']='subdetailadmin'
        
        return context


class ListSubAdmin(ListView):
    model = User
    template_name = 'trade_admin_auth/sub_admin_list.html'
    def get_queryset(self, **kwargs):
      return User.objects.filter(admin_user_profile__role=1)
    
    def get_context_data(self,**kwargs):
        context=super(ListSubAdmin, self).get_context_data(**kwargs)
        context['Title'] = 'Sub Admin List'
        subadmin_qs = User.objects.filter(admin_user_profile__role=1)
        context['subadmin_qs'] =subadmin_qs
        SubadminTable = SubAdminTable(subadmin_qs)
        context['table'] = SubadminTable
        context['activecls']='subdetailadmin'
        return context



class CreateSubadminUser(CreateView):
    form_class = AdminUserAddMultiForm
    template_name = 'trade_admin_auth/subadmin_add_form.html'
    raise_exception  = True
    def get_context_data(self, **kwargs):
       context = super(CreateSubadminUser, self).get_context_data(**kwargs)
       user_id = self.request.user.id
       menuqs = MenuModule.objects.filter(status = 0)
       context['Title'] = 'Create SubAdmin'
       context['Btn_url']='trade_admin_auth:subadminlist'
       context['activecls']='subdetailadmin'
       context['menuqs']=menuqs
       context['menu_qs_count'] = menuqs.count()
       return context
    
    @method_decorator(check_group("Manage Sub Admin"))
    def dispatch(self, *args, **kwargs):
      return super(CreateSubadminUser, self).dispatch(*args, **kwargs)
    
    @transaction.atomic
    def form_valid(self, form):
        form1 = form['form1']
        form2 = form['form2']
        get_email = form2.cleaned_data["emailaddress"]
        form1.instance.email = get_email
        form1.instance.is_staff = 1
        form1.instance.is_superuser = 1
        user_form = form1.save()
        
        encypt_email=encrypt_with_common_cipher(get_email)
        user_id=user_form.id
        group = Group.objects.get(name='Sub Admin')
        user_form.groups.add(group)
        
        
        form2.instance.user = user_form
        form2.instance.role=1
        form2.instance.emailaddress=encypt_email
        form2.instance.status=1
        form2.save()
        menu_perm_val = self.request.POST.get('menu_perm_list')
        obj_val = json.loads(menu_perm_val)
        list_val = []
        for item in obj_val.values():
          for i in item:
            list_val.append(int(i))
        menu_qs = MenuModule.objects.all()
        for j in menu_qs:
          if j.id in list_val:
            create_menu_permissions(self.request,user_id,j.id,0)
          else:
            create_menu_permissions(self.request,user_id,j.id,1)
        messages.add_message(self.request, messages.SUCCESS, 'Subadmin  created Successfully.')
        return HttpResponseRedirect('/tradeadmin/subadmin_sub_menu_add/'+str(user_id)+'/')

@check_group("Manage Sub Admin")
def CreateSubAdmin_SubMenu_User(request,id):
  context = {}
  context["Title"] = "Create Sub Menu Permission"
  user_obj = User.objects.get(id = id)
  user_obj_perm_id = MenuPermission.objects.filter(user_permissions_id = user_obj.id).filter(access_status = 0)
  menu_list = []
  for item in user_obj_perm_id:
    obj_sub_menu = SubMenuModule.objects.filter(main_module_name_id = item.access_modules.id)
    for item1 in obj_sub_menu:
      menu_list.append(str(item1.sub_module_name))
  context["obj_sub_menu"] = menu_list
  context["menu_qs_count"] = len(menu_list)

  if request.method == "POST":
    menu_perm_val = request.POST.get('menu_perm_list')
    obj_val = json.loads(menu_perm_val)
    list_val = []
    for item in obj_val.values():
      for i in item:
        list_val.append(str(i))
    menu_qs_sub = SubMenuModule.objects.all()
    for j in menu_qs_sub:
      if j.sub_module_name in list_val:
        menu_sub_obj = SubMenuModule.objects.get(sub_module_name = j.sub_module_name)
        menu_qs = MenuModule.objects.get(id = menu_sub_obj.main_module_name.id)
        menu_perm_qs = MenuPermission.objects.get(access_modules_id= menu_qs.id,user_permissions = user_obj.id)
        # for menu in menu_perm_qs:
        SubMenuPermission.objects.create(
          user_permissions_id=user_obj.id,
          main_access_modules_id = menu_perm_qs.id,
          sub_menu_name = menu_sub_obj,
          access_permissions=0,
          access_status = 0,
          created_on=datetime.datetime.now(),
          created_by_id = request.user.id,
          modified_by_id = request.user.id
        )  
      else:
        # for menu in menu_perm_qs:
        menu_sub_obj = SubMenuModule.objects.get(sub_module_name = j.sub_module_name)
        menu_qs = MenuModule.objects.get(id = menu_sub_obj.main_module_name.id)
        menu_perm_qs = MenuPermission.objects.get(access_modules_id= menu_qs.id,user_permissions = user_obj.id)
        SubMenuPermission.objects.create(
          user_permissions_id=user_obj.id,
          main_access_modules_id = menu_perm_qs.id,
          sub_menu_name = menu_sub_obj,
          access_permissions=0,
          access_status = 1,
          created_on=datetime.datetime.now(),
          created_by_id = request.user.id,
          modified_by_id = request.user.id
        ) 
    messages.add_message(request, messages.SUCCESS, 'Sub Menu access given Successfully.')
    return HttpResponseRedirect('/tradeadmin/subadminlist/')
  return render(request,'trade_admin_auth/subadmin_submenu_add_form.html', context)


@check_group("Manage Sub Admin")
def edit_subadmin_profilesetting(request,user_id):
    context={}
    user= User.objects.get(id=user_id)
    usermail = user.email
    userprofile= AdminUser_Profile.objects.get(user=user.id)
    user_profile_id = userprofile.id
    user_decrypt_emailaddress =userprofile.emailaddress  
    decrypt_user_emailaddress=decrypt_with_common_cipher(user_decrypt_emailaddress)
    if request.method == 'POST':
        profile_form = SubAdminUserProfileeditform(request.POST,instance=userprofile)
        getemail = request.POST['email']
        if getemail and User.objects.filter(Q(email=getemail) & Q(is_superuser=False)).count() > 0:
            messages.add_message(request, messages.ERROR, "This Email Address Already Registered")
            return HttpResponseRedirect('/tradeadmin/sub_admin_profile_settings/'+str(user_id)+'/')
        else:
            if profile_form.is_valid():
              
              getusername = request.POST['username']
              userupdateform = User.objects.filter(id=user_id).update(email = getemail , username = getusername)
              get_emailaddress = getemail
              profile_form.instance.created_by_id = request.user.id
              profile_form.instance.modified_by_id = request.user.id
              profile_form.save()
              if get_emailaddress != "":
                encrypt_useremail=encrypt_with_common_cipher(get_emailaddress)
                update_emailaddress = AdminUser_Profile.objects.get(id = user_profile_id)
                update_emailaddress.emailaddress = encrypt_useremail
                update_emailaddress.save()
                
              else:
                messages.add_message(request, messages.ERROR, 'Email address must required.')
                return HttpResponseRedirect('/tradeadmin/sub_admin_profile_settings/'+str(user_id)+'/')
              messages.add_message(request, messages.SUCCESS, 'Sub Admin Profile updated Successfully.')
              return HttpResponseRedirect('/tradeadmin/sub_admin_profile_settings/'+str(user_id)+'/')
            else:
              messages.add_message(request, messages.ERROR, "gfhd")
              return HttpResponseRedirect('/tradeadmin/sub_admin_profile_settings/'+str(user_id)+'/')
    else:
        context={
            'Title':'Profile Setting',
            'decrypt_user_emailaddress':decrypt_user_emailaddress,
            'usermail':usermail,
            'user' : user
          }
    return render(request,'trade_admin_auth/subadmin_edit_profile.html', context)

def SubAdminChangePasswordView(request,user_id):
    context={}
    user = User.objects.get(id = user_id)
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            auth.update_session_auth_hash(request, form)
            messages.add_message(request, messages.SUCCESS, 'Change password updated Successfully.')
            return HttpResponseRedirect('/tradeadmin/subadmin_change_password/'+str(user_id)+'/')
        else:
            messages.add_message(request, messages.ERROR, 'Password Does Not Match.')
            return HttpResponseRedirect('/tradeadmin/subadmin_change_password/'+str(user_id)+'/')
    else:
        form = SetPasswordForm(user)
    context['user'] = user
    context['Title']= 'Change Password'
    return render(request,'trade_admin_auth/subadmin_changepassword.html',context)

@check_group("Manage Sub Admin")
def sub_adminchange_pattern_view(request,user_id):
    context={}
    
    user= User.objects.get(id=user_id)
    user_profile_id = user.admin_user_profile.id
    user_profile_pattern = user.admin_user_profile.pattern_code
    if request.method == 'POST':
       pattern_code = int(request.POST['pattern_code'])
       oldpattern = int(request.POST['old_pattern_code'])
       confirmpattern = int(request.POST['confirmpattern_code'])
       if oldpattern != "" and oldpattern == user_profile_pattern:
        if oldpattern !="" and confirmpattern != "" and pattern_code != "":
          if pattern_code == confirmpattern:
           if pattern_code != "": 
              update_patterncode = AdminUser_Profile.objects.get(id = user_profile_id)
              update_patterncode.pattern_code = pattern_code
              update_patterncode.save()
              messages.add_message(request, messages.SUCCESS, 'Change pattern updated Successfully.')
           else:
              messages.add_message(request, messages.ERROR, 'New pattern must required.')
              return HttpResponseRedirect('/tradeadmin/subadmin_patternchange/'+str(user_id)+'/')
         
          else:
            messages.add_message(request, messages.ERROR, 'Confirm pattern is mismatch')
            return HttpResponseRedirect('/tradeadmin/subadmin_patternchange/'+str(user_id)+'/')
        else:
          messages.add_message(request, messages.ERROR, 'Pattern Code must required')
          return HttpResponseRedirect('/tradeadmin/subadmin_patternchange/'+str(user_id)+'/')
       else:
        messages.add_message(request, messages.ERROR, 'Old pattern is mismatch')
        return HttpResponseRedirect('/tradeadmin/subadmin_patternchange/'+str(user_id)+'/')
       
       return HttpResponseRedirect('/tradeadmin/subadmin_patternchange/'+str(user_id)+'/')
    else:
          
        
        context={
            'Title':'Change Pattern',
            'patterncode':user_profile_pattern,
            'user' : user
           }
        
    return render(request,'trade_admin_auth/subadmin_changepattern.html', context)


@check_group("Manage Sub Admin")
def SubadminEditPermission(request,user_id):
  context = {}
  user= User.objects.get(id=user_id)
  menuqs = MenuPermission.objects.filter(user_permissions_id = user.id)
  context['Title'] = 'Menu Permissions'
  context['menuqs']=menuqs
  context["user"] = user
  context['menu_qs_count'] = menuqs.count()
  if request.method =="POST":
    menu_perm_val = request.POST.get('menu_perm_list')
    obj_val = json.loads(menu_perm_val)
    list_val = []
    for item in obj_val.values():
      for i in item:
         if i is not None:
            list_val.append(int(i))
    menu_qs = MenuPermission.objects.filter(user_permissions_id = user.id)
    for j in menu_qs:
      if j.id in list_val:
        MenuPermission.objects.filter(id = j.id).update(access_status = 0)  
      else:
        MenuPermission.objects.filter(id = j.id).update(access_status = 1) 
    messages.add_message(request, messages.SUCCESS, 'Permission  updated Successfully.')
    return HttpResponseRedirect('/tradeadmin/subadmin_edit_permission/'+str(user.id)+'/')
  return render(request,'trade_admin_auth/subadmin_permissions.html',context)


@check_group("Manage Sub Admin")
def Subadmin_SubMenu_EditPermission(request,user_id):
  context = {}
  user= User.objects.get(id=user_id)
  menuqs = SubMenuPermission.objects.filter(user_permissions_id = user.id)
  context['Title'] = 'Sub Menu Permissions'
  context['menuqs']=menuqs
  context["user"] = user
  context['menu_qs_count'] = menuqs.count()
  if request.method =="POST":
    menu_perm_val = request.POST.get('menu_perm_list')
    obj_val = json.loads(menu_perm_val)
    list_val = []
    for item in obj_val.values():
      for i in item:
        list_val.append(int(i))
    menu_qs = SubMenuPermission.objects.filter(user_permissions_id = user.id)
    for j in menu_qs:
      if j.id in list_val:
        SubMenuPermission.objects.filter(id = j.id).update(access_status = 0)  
      else:
        SubMenuPermission.objects.filter(id = j.id).update(access_status = 1) 
    messages.add_message(request, messages.SUCCESS, 'Sub Menu Permission updated Successfully.')
    return HttpResponseRedirect('/tradeadmin/subadmin_submenu_edit_permission/'+str(user.id)+'/')
    
  return render(request,'trade_admin_auth/subadmin_submenu_edit_permission.html', context)


class EditSubadmin(UpdateView):    
    model=User
    form_class = AdminUserEditSubadminMultiForm
    template_name = 'trade_admin_auth/subadmin_editform.html'
    def get_context_data(self, **kwargs):
       context = super(EditSubadmin, self).get_context_data(**kwargs)
       context['Title']='Edit Subadmin'
       context['activecls']='subdetailadmin'
       context['Btn_url'] = 'trade_admin_auth:subadminlist'
       return context
    def get_form_kwargs(self):
        kwargs = super(EditSubadmin, self).get_form_kwargs()
        kwargs.update(instance={
            'form1': self.object,
            'form2': self.object.admin_user_profile,
        })
        return kwargs
    def get_success_url(self, **kwargs):
        p_key = int(self.kwargs['pk'])
        messages.add_message(self.request, messages.SUCCESS, 'Subadmin details updated Successfully.')
        return '{}'.format(reverse('trade_admin_auth:subadminlist'))
def create_menu_permissions(request,user_id,list_val,access_status):
    menu_perm_val = list_val
    create_menu = MenuPermission.objects.create(
      user_permissions_id=user_id,
      access_modules_id=menu_perm_val,
      access_permissions=0,
      access_status = access_status,
      created_on=datetime.datetime.now(),
      created_by_id = request.user.id,
      modified_by_id = request.user.id

    )   

    return  True


def SubAdmin_FormView(request,user_id):
    context={}
    user= User.objects.get(id=user_id)
    menu_permission_qs = MenuPermission.objects.filter(user_permissions = user_id)
    if request.method == 'POST':
       messages.add_message(request, messages.SUCCESS, 'Assign permissions successfully updated.')
       return HttpResponseRedirect('/tradeadmin/subadminlist/')
    else:
        context={
            'Title':'Assign Permissions',
            'menu_permission_qs':menu_permission_qs,
            'activecls':'subdetailadmin'
           }
        
    return render(request,'trade_admin_auth/subadmin_permissions.html', context)



class DeleteSubAdmin(SubAdminRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        
        user_qs = get_object_or_404(User, pk=pkey)
        if user_qs.is_active == False:
            user_qs.is_active = True
            status = 'activated'
        elif user_qs.is_active == True:    
            user_qs.is_active = False
            status = 'deactivated'
        user_qs.save()
        
        messages.add_message(request, messages.SUCCESS, 'SubAdmin '+status+' status updated successfully.') 
        return HttpResponseRedirect(reverse('trade_admin_auth:subadminlist'))



class DeleteTwoFAAdmin(ManageUserAdminRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(User, pk=pkey)
        get_userprofile = AdminUser_Profile.objects.get(user = user_qs.id)
        if get_userprofile.twofa == True:
          get_userprofile.twofa = False
          get_userprofile.save()
        
        messages.add_message(request, messages.SUCCESS, 'User twofa  status updated successfully.') 
        return HttpResponseRedirect(reverse('trade_admin_auth:twofalist'))



class ListTradeUserAdmin(ManageUserAdminRequiredMixin,ListView):
    model = User
    template_name = 'trade_admin_auth/manage_user_list.html'
    def get_queryset(self, **kwargs):
      return User.objects.filter(Q(admin_user_profile__role=2) & Q(is_active=True)).order_by('-id')
    def get_context_data(self,**kwargs):
        context=super(ListTradeUserAdmin, self).get_context_data(**kwargs)
        context['Title'] = 'User List'
        tradeuser_qs = User.objects.filter(Q(admin_user_profile__role=2) & Q(is_active=True)).order_by('-id')
        context['tradeuser_qs'] =tradeuser_qs
        contenttable = TradeUserTable(tradeuser_qs)
        context['table'] = contenttable
        context['Reset_url'] = 'trade_admin_auth:tradeuserlist'
        context['activecls']='userdetailadmin'
        return context




class ListTradeDeactiveUserAdmin(BlockIpaddressAdminRequiredMixin,ListView):
    model = User
    template_name = 'trade_admin_auth/deactivateuser_list.html'
    def get_queryset(self, **kwargs):
      return User.objects.filter(Q(admin_user_profile__role=2) & Q(is_active=False) & (Q(admin_user_profile__status=2) | Q(admin_user_profile__status=0))).order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(ListTradeDeactiveUserAdmin, self).get_context_data(**kwargs)
        context['Title'] = 'Deactivate User List'
        tradeuser_qs = User.objects.filter(Q(admin_user_profile__role=2) & Q(is_active=False) & (Q(admin_user_profile__status=2) | Q(admin_user_profile__status=0))).order_by('-id')
        context['subadmin_qs'] =tradeuser_qs
        deativateuser=DeactivateUserTable(tradeuser_qs)
        context['table'] = deativateuser
        context['activecls']='userdetailadmin'
        return context


class ListTwoFAUserAdmin(BlockIpaddressAdminRequiredMixin,ListView):
    model = User
    template_name = 'trade_admin_auth/2fauserlist.html'
    def get_queryset(self, **kwargs):
      return User.objects.filter(Q(admin_user_profile__role=2)).order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(ListTwoFAUserAdmin, self).get_context_data(**kwargs)
        context['Title'] = 'TwoFA User List'
        tradeuser_qs = User.objects.filter(Q(admin_user_profile__role=2)).order_by('-id')
        context['subadmin_qs'] =tradeuser_qs
        deativateuser=DeactivateUserTable(tradeuser_qs)
        context['table'] = deativateuser
        context['activecls']='userdetailadmin'
        return context


class DeleteTradeuserAdmin(BlockIpaddressAdminRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(User, pk=pkey)
        user_id = user_qs.id
        get_userprofile = AdminUser_Profile.objects.get(user = user_id)
        if user_qs.is_active == False:
            user_qs.is_active = True
            get_userprofile.status = 1
            get_userprofile.save()
            status = 'activated'
            messages.add_message(request, messages.SUCCESS, 'User Activate status updated successfully.') 
        elif user_qs.is_active == True:    
            user_qs.is_active = False
            get_userprofile.status = 2
            get_userprofile.save()
            messages.add_message(request, messages.ERROR, 'User Deactivate status updated successfully.')
            status = 'deactivated'
        user_qs.save()
        
        
        return HttpResponseRedirect(reverse('trade_admin_auth:tradeuserlist'))


class DetailTradeUser(BlockIpaddressAdminRequiredMixin,DetailView):
    model = User 
    template_name = 'trade_admin_auth/user_profile.html'
    def get_context_data(self, **kwargs):
       context = super(DetailTradeUser, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       user_qs = User.objects.get(id=p_key)
       context['Title'] = 'User Info'
       context['user_qs']=user_qs
       context['activecls']='userdetailadmin'

       return context

class ListUseractivity(BlockIpaddressAdminRequiredMixin,ListView):
    model = AdminUser_Activity
    template_name = 'trade_admin_auth/tradeuseractivitylist.html'
    def get_queryset(self, **kwargs):
      return AdminUser_Activity.objects.filter(user__admin_user_profile__role=2).order_by('-id')
    def get_context_data(self,**kwargs):
        context=super(ListUseractivity, self).get_context_data(**kwargs)
        context['Title'] = 'User Login History'
        tradeuser_qs = AdminUser_Activity.objects.filter(user__admin_user_profile__role=2).order_by('-id')
        context['tradeuser_qs'] =tradeuser_qs
        contenttable = AdminActivityTable(tradeuser_qs)        
        context['table'] = contenttable
        RequestConfig(self.request, paginate={'per_page': 15}).configure(contenttable)
        context['Reset_url'] = 'trade_admin_auth:activityuserlist'
        context['activecls']='userdetailadmin'
        
        return context 



class ListBlockIp(BlockIpaddressAdminRequiredMixin,ListView):
    model = Blockip
    template_name = 'trade_admin_auth/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return Blockip.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(ListBlockIp, self).get_context_data(**kwargs)
        context['Title'] = 'Block IPAddress'
        adminactivity_qs = Blockip.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = BlockIPTable(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add BlockIp'
        context['Btn_url'] = 'trade_admin_auth:addblockip'
        return context


class AddBlockIp(BlockIpaddressAdminRequiredMixin,CreateView):
    model = Blockip
    form_class = BlockipForm
    template_name = 'trade_admin_auth/addblockip.html'   
    def get_context_data(self, **kwargs):
       context = super(AddBlockIp, self).get_context_data(**kwargs)
       context['Title'] = 'Add Blockip'
       context['Btn_url'] = 'trade_admin_auth:blockiplist'
       return context

    @transaction.atomic
    def form_valid(self, form):
        
       form.instance.created_on   = datetime.datetime.now()
       form.instance.created_by_id = self.request.user.id
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()
       
       messages.add_message(self.request, messages.SUCCESS, 'Blockip created successfully.')
       return HttpResponseRedirect('/tradeadmin/blockiplist/')


class EditBlockIp(BlockIpaddressAdminRequiredMixin,UpdateView):
    model = Blockip
    form_class = BlockipForm
    template_name = 'trade_admin_auth/editblockip.html'   
    def get_context_data(self, **kwargs):
       context = super(EditBlockIp, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       context['Title'] = 'Edit BlockIP'
       context['Btn_url'] = 'trade_admin_auth:blockiplist'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Blockip updated successfully.')
       return HttpResponseRedirect('/tradeadmin/blockiplist/')



class ListAttemptIPBlock(BlockIpaddressAdminRequiredMixin,ListView):
    model = AccessAttempt
    template_name = 'trade_admin_auth/attemptlist.html'
    def get_queryset(self, **kwargs):
      return AccessAttempt.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(ListAttemptIPBlock, self).get_context_data(**kwargs)
        context['Title'] = 'Attempt Block IPAddress'
        attempt_qs = AccessAttempt.objects.all().order_by('-id')
        context['attempt_qs'] =attempt_qs
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        context['ip'] = ip
        return context

class DeleteAttemptIPBlock(BlockIpaddressAdminRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        
        user_qs = get_object_or_404(AccessAttempt, pk=pkey)
        user_qs.delete()
        messages.add_message(request, messages.SUCCESS, 'Attempt BlockIP Address deleted successfully.') 
        return HttpResponseRedirect(reverse('trade_admin_auth:attemptiplist'))
'''
class ListUserAddress(ListView):
    model = UserAddress
    template_name = 'trade_admin_auth/generic_list.html'
    def get_queryset(self, **kwargs):
      return UserAddress.objects.all().order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(ListUserAddress, self).get_context_data(**kwargs)
        context['Title'] = 'User Address List'
        content_qs = UserAddress.objects.all().order_by('-id')
        context['content_qs'] =content_qs
        contenttable = UserAddressTable(content_qs)
        context['table'] = contenttable
        context['activecls']='useraddressadmin'
        return context
'''

def get_hbdtoken(request):
  try:
    hbdtoken = TradeCurrency.objects.get(Q(symbol='HBD'))
  except TradeCurrency.DoesNotExist:
    hbdtoken = ''
  return hbdtoken
'''
class WalletDetail(DetailView):
    model = UserAddress 
    template_name = 'trade_admin_auth/wallet_detail.html'
    def get_context_data(self, **kwargs):
       context = super(WalletDetail, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = UserAddress.objects.get(id=p_key)
       context['Title'] = 'User Address Detail'
       context['staticcontent_qs']=staticcontent_qs
       wallet_qs = UserWallet.objects.filter(useraddress = staticcontent_qs.id)
       context['wallet_qs']=wallet_qs
       bid_qs = Bids.objects.filter(useraddress = staticcontent_qs.id)
       total_bid_qs = Bids.objects.filter(useraddress = staticcontent_qs.id).count()
       bid_token_values = bid_qs.aggregate(bidtokensum=Sum('bidamount'))
       bid_token = bid_token_values['bidtokensum'] if bid_token_values['bidtokensum'] else Decimal(0)
       total_winning_bid_qs = Bids.objects.filter(Q(useraddress = staticcontent_qs.id) & Q(status=1)).count()
       try:
            hbdtoken = TradeCurrency.objects.get(Q(symbol='HBD'))
       except TradeCurrency.DoesNotExist:
            hbdtoken = ''
       context['hbdtoken']=hbdtoken
       context['bid_qs']=bid_qs
       context['total_bid_qs'] = total_bid_qs
       context['bid_token']=bid_token
       context['total_winning_bid_qs']=total_winning_bid_qs
       context['activecls']='useraddressadmin'
       return context

'''

# def scheme_master(request):
#   context={}
#   context['Title'] = 'Scheme Master'
#   if request.method == "POST": 
#     scheme_name = request.POST.get('scheme_name')
#     scheme_type = request.POST.get('scheme_type')
#     if scheme_name:
#       scheme_master.objects.create(Scheme_name=scheme_name,Scheme_type=scheme_type)
#       messages.success(request, 'Create Successfully!')
#       return HttpResponseRedirect('/tradeadmin/scheme_master/')
#     else:
#       messages.add_message(request, messages.ERROR, 'Field Required!!!!!')
#   return render(request,'trade_admin_auth/scheme_master.html',context)

class schememaster(BlockIpaddressAdminRequiredMixin,CreateView):
    model = Scheme
    form_class = scheme_master_Form
    template_name = 'trade_admin_auth/scheme_master.html'   
    def get_context_data(self, **kwargs):
       context = super(schememaster, self).get_context_data(**kwargs)
       context['Title'] = 'Scheme Master'
       context['Btn_url'] = 'trade_admin_auth:scheme_master'
       return context

    @transaction.atomic
    def form_valid(self, form):
        sch_name=form.instance.Scheme_name
        form.instance.created_on = datetime.datetime.now()
        form.instance.modified_on = datetime.datetime.now()
        if sch_name: 
          formsave = form.save()
          messages.success(self.request, 'Scheme Created Successfully.')
        else:
          messages.error(self.request, 'Field Required!!!!.')
        return HttpResponseRedirect(reverse_lazy('trade_admin_auth:scheme_master'))
        
def getschemedetails(request):
  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  obj_username = Scheme.objects.raw('SELECT id, Scheme_name, Scheme_type FROM SCHzWkaJsitsYeR ORDER BY id DESC LIMIT %s, %s',[start, length])
  serializer = scheme_Serializer(obj_username, many=True)
  for total_count in Scheme.objects.raw('SELECT id, COUNT(*) as counts FROM SCHzWkaJsitsYeR ORDER BY counts'):
    totalRecords = total_count.counts
    set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
    tt = (list(set_object))
    tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})

def amout_mast(request):
  context={}
  context['Title'] = 'Amount Master'
  obj_user=Scheme.objects.all()
  context['obj_user'] = obj_user
  if request.method == "POST":
    name = request.POST["scheme_name"]
    amount = request.POST["amount"]
    number = request.POST["number"]
    status = request.POST["status"]
    obj_sch=Scheme.objects.get(Scheme_name=name)
    Scheme_amount_master.objects.create(Scheme_id=obj_sch.id,Scheme_name=name,Scheme_amount=amount,user_count=number,status=status)
    messages.success(request, 'Amount Update Successfully.')
  return render(request,'trade_admin_auth/amount_master.html',context)



def getschemeamount(request):
  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  obj_username = Scheme_amount_master.objects.raw('SELECT id,Scheme_id,Scheme_name,Scheme_amount,user_count,status FROM SCHAMTWkaJtsYeR ORDER BY id DESC LIMIT %s, %s',[start, length])
  serializer = scheme_amount_Serializer(obj_username, many=True)
  for total_count in Scheme_amount_master.objects.raw('SELECT id, COUNT(*) as counts FROM SCHAMTWkaJtsYeR ORDER BY counts'):
    totalRecords = total_count.counts
    set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
    tt = (list(set_object))
    tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})


def gold_mast(request):
  context={}
  context['Title'] = 'Gold Master'
  if request.method == "POST":
    name = request.POST["name"]
    amount = request.POST["amount"]
    date = request.POST["plan_end_date"]
    Gold_master.objects.create(Metal_name=name,Metal_amount=amount,Metal_id=date)
    messages.success(request, 'Update Successfully!!!!!')
  return render(request,'trade_admin_auth/gold_master.html',context)

    

def getschemegold(request):
  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  obj_username = Gold_master.objects.raw('SELECT id,Metal_id,Metal_name,Metal_amount,created_on FROM GOLjkghsiJtiuo ORDER BY id DESC LIMIT %s, %s',[start, length])
  serializer = gold_amount_Serializer(obj_username, many=True)
  for total_count in Gold_master.objects.raw('SELECT id, COUNT(*) as counts FROM GOLjkghsiJtiuo ORDER BY counts'):
    totalRecords = total_count.counts
    set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
    tt = (list(set_object))
    tt.sort(reverse=False) 
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})


