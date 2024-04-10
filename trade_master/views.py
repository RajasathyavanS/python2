from django.shortcuts import render
from django.shortcuts import render,get_list_or_404, get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect


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

from Crypto.Cipher import AES
import base64
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

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



from django.template.loader import get_template
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from company.models import Company


from trade_admin_auth.mixins import check_group
from trade_admin_auth.mixins import CmsAdminRequiredMixin,FaqAdminRequiredMixin,ContactusAdminRequiredMixin
from trade_admin_auth.mixins import EmailTemplateAdminRequiredMixin,RoadmapAdminRequiredMixin,CurrencyAdminRequiredMixin



from trade_master.models import Cms_StaticContent,Faq,Contactus,EmailTemplate,Roadmap,Currencylist,AccessLog
from trade_master.forms import ContentPageForm,FaqForm,ContactForm,EmailContentForm,RoadmapForm,CurrencyForm

from trade_master.tables import StaticContentTable,CmsContentTable,FaqTable,ContactusTable
from trade_master.tables import EmailTemplateTable,RoadmapTable,CurrencyTable


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

def decrypt_with_common_cipher(ciphertext):
    common_cipher = get_common_cipher()
    raw_ciphertext = base64.b64decode(ciphertext)
    decrypted_message_with_padding = common_cipher.decrypt(raw_ciphertext)
    return decrypted_message_with_padding.decode('utf-8').strip()




class Liststaticcontent(CmsAdminRequiredMixin,ListView):
    model = Cms_StaticContent
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Cms_StaticContent.objects.filter(contenttype=0)
    
    def get_context_data(self,**kwargs):
        context=super(Liststaticcontent, self).get_context_data(**kwargs)
        context['Title'] = 'CMS Page'
        content_qs = Cms_StaticContent.objects.filter(contenttype=0)
        context['content_qs'] =content_qs
        contenttable = StaticContentTable(content_qs)
        context['table'] = contenttable
        context['activecls']='cmsstaticadmin'
        return context



class UpdateCms_StaticContent(CmsAdminRequiredMixin,UpdateView):
    model = Cms_StaticContent
    form_class = ContentPageForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateCms_StaticContent, self).get_context_data(**kwargs)
       context['Title'] = 'Cms Page'
       context['Btn_url'] = 'trade_master:cmspagelist'
       context['activecls']='cmsstaticadmin'
       return context

    @transaction.atomic
    def form_valid(self, form):
       
       form.instance.modified_by_id = self.request.user.id
       form.instance.contenttype =0
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'cms page updated successfully.')
       return HttpResponseRedirect('/trademaster/cmspagelist/')


class DetailStaticcontent(CmsAdminRequiredMixin,DetailView):
    model = Cms_StaticContent 
    template_name = 'trade_master/cms_detail.html'
    def get_context_data(self, **kwargs):
       context = super(DetailStaticcontent, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Cms_StaticContent.objects.get(id=p_key)
       context['Title'] = 'Cms Page Detail'
       context['staticcontent_qs']=staticcontent_qs
       context['activecls']='cmsstaticadmin'
       return context

class Listcontent(CmsAdminRequiredMixin,ListView):
    model = Cms_StaticContent
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Cms_StaticContent.objects.filter(Q(contenttype=1) & Q(status=0))
    
    def get_context_data(self,**kwargs):
        context=super(Listcontent, self).get_context_data(**kwargs)
        context['Title'] = 'CMS Home Content'
        content_qs = Cms_StaticContent.objects.filter(Q(contenttype=1) & Q(status=0))
        context['content_qs'] =content_qs
        contenttable = CmsContentTable(content_qs)
        context['table'] = contenttable
        context['activecls']='cmsstaticadmin'
        return context



class UpdateCms_Content(CmsAdminRequiredMixin,UpdateView):
    model = Cms_StaticContent
    form_class = ContentPageForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateCms_Content, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       staticcontent_qs = Cms_StaticContent.objects.get(id=p_key)
       context['Title'] = 'Cms Home Content'
       context['staticcontent_qs']=staticcontent_qs
       context['Btn_url'] = 'trade_master:cmspagecontentlist'
       context['activecls']='cmsstaticadmin'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       form.instance.contenttype =1
       formsave=form.save()
       messages.add_message(self.request, messages.SUCCESS, 'cms content updated successfully.')
       return HttpResponseRedirect('/trademaster/cmspagecontentlist/')


class Detailcontent(CmsAdminRequiredMixin,DetailView):
    model = Cms_StaticContent 
    template_name = 'trade_master/cms_content_detail.html'
    def get_context_data(self, **kwargs):
       context = super(Detailcontent, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       staticcontent_qs = Cms_StaticContent.objects.get(id=p_key)
       context['Title'] = 'Cms Home Content Detail'
       context['staticcontent_qs']=staticcontent_qs
       context['activecls']='cmsstaticadmin'
       return context


class ListFaq(FaqAdminRequiredMixin,ListView):
    model = Faq
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return Faq.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(ListFaq, self).get_context_data(**kwargs)
        context['Title'] = 'FAQ'
        content_qs = Faq.objects.all()
        context['content_qs'] =content_qs
        contenttable = FaqTable(content_qs)
        context['table'] = contenttable
        context['add_title'] ='Add FAQ'
        context['Btn_url'] = 'trade_master:addfaq'
        return context

class AddFaq(FaqAdminRequiredMixin,CreateView):
    model = Faq
    form_class = FaqForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(AddFaq, self).get_context_data(**kwargs)
       context['Title'] = 'Add FAQ'
       context['Btn_url'] = 'trade_master:faqlist'
       return context

    @transaction.atomic
    def form_valid(self, form):
        
       form.instance.created_on   = datetime.datetime.now()
       form.instance.created_by_id = self.request.user.id
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()
       form.instance.name = formsave.title
       form.save()

       messages.add_message(self.request, messages.SUCCESS, 'faq created successfully.')
       return HttpResponseRedirect('/trademaster/faqlist/')

class UpdateFaq(FaqAdminRequiredMixin,UpdateView):
    model = Faq
    form_class = FaqForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateFaq, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       staticcontent_qs = Faq.objects.get(id=p_key)
       context['Title'] = 'Update FAQ'
       context['Btn_url'] = 'trade_master:faqlist'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()
       form.instance.created_by_id = self.request.user.id
       form.instance.modified_by_id = self.request.user.id
       messages.add_message(self.request, messages.SUCCESS, 'faq updated successfully.')
       return HttpResponseRedirect('/trademaster/faqlist/')




class Detailfaq(FaqAdminRequiredMixin,DetailView):
    model = Faq 
    template_name = 'trade_master/faq_detail.html'
    def get_context_data(self, **kwargs):
       context = super(Detailfaq, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Faq.objects.get(id=p_key)
       context['Title'] = 'FAQ Detail'
       context['staticcontent_qs']=staticcontent_qs
       return context



class ListRoadmap(RoadmapAdminRequiredMixin,ListView):
    model = Roadmap
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return Roadmap.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(ListRoadmap, self).get_context_data(**kwargs)
        context['Title'] = 'RoadMap'
        content_qs = Roadmap.objects.all()
        context['content_qs'] =content_qs
        contenttable = RoadmapTable(content_qs)
        context['table'] = contenttable
        context['add_title'] ='Add Roadmap'
        context['Btn_url'] = 'trade_master:addroadmap'
        return context

class AddRoadmap(RoadmapAdminRequiredMixin,CreateView):
    model = Roadmap
    form_class = RoadmapForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(AddRoadmap, self).get_context_data(**kwargs)
       context['Title'] = 'Add Roadmap'
       context['Btn_url'] = 'trade_master:roadmaplist'
       return context

    @transaction.atomic
    def form_valid(self, form):
        
       form.instance.created_on   = datetime.datetime.now()
       form.instance.created_by_id = self.request.user.id
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()
       form.instance.name = formsave.title
       form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Roadmap created successfully.')
       return HttpResponseRedirect('/trademaster/roadmaplist/')

class UpdateRoadmap(RoadmapAdminRequiredMixin,UpdateView):
    model = Roadmap
    form_class = RoadmapForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateRoadmap, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       staticcontent_qs = Roadmap.objects.get(id=p_key)
       context['Title'] = 'Update Roadmap'
       context['Btn_url'] = 'trade_master:roadmaplist'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()
       messages.add_message(self.request, messages.SUCCESS, 'Roadmap updated successfully.')
       return HttpResponseRedirect('/trademaster/roadmaplist/')



class DetailRoadmap(RoadmapAdminRequiredMixin,DetailView):
    model = Roadmap 
    template_name = 'trade_master/roadmap_detail.html'
    def get_context_data(self, **kwargs):
       context = super(DetailRoadmap, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Roadmap.objects.get(id=p_key)
       context['Title'] = 'Roadmap Detail'
       context['staticcontent_qs']=staticcontent_qs
       return context



class Listcontactus(ContactusAdminRequiredMixin,ListView):
    model = Contactus
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Contactus.objects.filter(status=0).order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(Listcontactus, self).get_context_data(**kwargs)
        context['Title'] = 'Contacted User List'
        content_qs = Contactus.objects.filter(status=0).order_by('-id')
        context['content_qs'] =content_qs
        contenttable = ContactusTable(content_qs)
        context['table'] = contenttable
        return context


class UpdateContactus(ContactusAdminRequiredMixin,UpdateView):
    model = Contactus
    form_class = ContactForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateContactus, self).get_context_data(**kwargs)
       context['Title'] = 'Update Contact user'
       context['Btn_url'] = 'trade_master:contactlist'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.read_status = 1
       formsave=form.save()
       try:
        companyqs = Company.objects.get(id=1)
        companyname= companyqs.name
        copyright= companyqs.copy_right
        comp_logo = companyqs.company_logo
       except:
        companyqs = ''
        copyright = ''
        comp_logo=''
       email_template = EmailTemplate.objects.get(name ="contactus_reply")
       if email_template:
          email_template_qs =email_template
       else:
          email_template_qs = ''

       text_file = open("trade_master/templates/emailtemplate/contactus_reply.html", "w")  
       text_file.write(email_template.content)
       text_file.close()
       email_subject = email_template.Subject
       to_email = formsave.email
       from_email_get = settings.EMAIL_USER
       from_email =decrypt_with_common_cipher(from_email_get)
       hostuser = decrypt_with_common_cipher(settings.EMAIL_USER_ENC)
       hostpassword = decrypt_with_common_cipher(settings.EMAIL_PASSWORD_ENC)
       settings.EMAIL_HOST_USER = hostuser
       settings.EMAIL_HOST_PASSWORD = hostpassword
    
       data= {
          'username':formsave.name,
          'email':to_email,
          'company_logo':'comp_company_logo',
          'reply': formsave.reply,
          'company_logo':comp_logo,
          'copyright':copyright,
          'domain':get_current_site(self.request),
          }
       text_content = 'This is an important message.'
       htmly = get_template('emailtemplate/support_reply.html')
       html_content = htmly.render(data)
       msg = EmailMultiAlternatives(email_subject, text_content, from_email, [to_email])
       msg.attach_alternative(html_content, "text/html")
       msg.send()

       messages.add_message(self.request, messages.SUCCESS, 'reply message updated successfully.')
       return HttpResponseRedirect('/trademaster/contactlist/')


class Detailcontactus(ContactusAdminRequiredMixin,DetailView):
    model = Contactus 
    template_name = 'trade_master/contactus_detail.html'
    def get_context_data(self, **kwargs):
       context = super(Detailcontactus, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Contactus.objects.get(id=p_key)
       context['Title'] = 'Contact Info'
       context['staticcontent_qs']=staticcontent_qs
       return context





class Listemailcontent(EmailTemplateAdminRequiredMixin,ListView):
    model = EmailTemplate
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return EmailTemplate.objects.filter(status=0)
    
    def get_context_data(self,**kwargs):
        context=super(Listemailcontent, self).get_context_data(**kwargs)
        context['Title'] = 'Email Template List'
        content_qs = EmailTemplate.objects.filter(status=0)
        context['content_qs'] =content_qs
        contenttable = EmailTemplateTable(content_qs)
        context['table'] = contenttable
        return context

class Updateemailcontent(EmailTemplateAdminRequiredMixin,UpdateView):
    model = EmailTemplate
    form_class = EmailContentForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(Updateemailcontent, self).get_context_data(**kwargs)
       context['Title'] = 'Update Email Template'
       context['Btn_url'] = 'trade_master:emailcontactlist'
       return context

    @transaction.atomic
    def form_valid(self, form):
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Email content updated successfully.')
       return HttpResponseRedirect('/trademaster/emailcontactlist/')


class ListCurrencyDetails(CurrencyAdminRequiredMixin,ListView):
    model = Currencylist
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Currencylist.objects.filter(status=0)
    
    def get_context_data(self,**kwargs):
        context=super(ListCurrencyDetails, self).get_context_data(**kwargs)
        context['Title'] = 'List of currency'
        content_qs = Currencylist.objects.filter(status=0)
        context['content_qs'] =content_qs
        contenttable = CurrencyTable(content_qs)
        context['table'] = contenttable
        return context


class Updatecurrency(CurrencyAdminRequiredMixin,UpdateView):
    model = Currencylist
    form_class = CurrencyForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(Updatecurrency, self).get_context_data(**kwargs)
       context['Title'] = 'Edit Currency'
       context['Btn_url'] = 'trade_master:currencylist'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()
       messages.add_message(self.request, messages.SUCCESS, 'Currency updated successfully.')
       return HttpResponseRedirect('/trademaster/currencylist/')


class Detailcurrency(CurrencyAdminRequiredMixin,DetailView):
    model = Currencylist 
    template_name = 'trade_master/currency_detail.html'
    def get_context_data(self, **kwargs):
       context = super(Detailcurrency, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Currencylist.objects.get(id=p_key)
       context['Title'] = 'Currency Detail'
       context['staticcontent_qs']=staticcontent_qs
       return context 