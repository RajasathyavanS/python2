from django.contrib import admin

from trade_admin_auth.models import AdminUser_Profile,AdminUser_Activity,AccessAttempt


admin.site.register(AdminUser_Profile)
admin.site.register(AdminUser_Activity)
admin.site.register(AccessAttempt)