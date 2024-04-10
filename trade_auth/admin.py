from django.contrib import admin
from trade_auth.models import UserAddress,UserWallet

admin.site.register(UserAddress)
admin.site.register(UserWallet)