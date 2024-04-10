from django.contrib import admin
from trade_master.models import Cms_StaticContent,Faq,Contactus,EmailTemplate
from auditable.views import AuditableAdminMixin

from trade_master.models import Roadmap,Currencylist,Blockip

class Cms_StaticContentAdmin(AuditableAdminMixin):
    model = Cms_StaticContent
    list_display = ['id','name','title','content','status']
    
admin.site.register(Cms_StaticContent,Cms_StaticContentAdmin)
admin.site.register(Faq)
admin.site.register(Contactus)
admin.site.register(EmailTemplate)
admin.site.register(Roadmap)
admin.site.register(Currencylist)
admin.site.register(Blockip)
