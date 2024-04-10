from rest_framework import serializers
from locations.models import Country,State
from trade_master.models import Cms_StaticContent, Faq
from trade_admin_auth.models import Gold_master, Scheme, Scheme_amount_master

class scheme_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Scheme
        fields=['id','Scheme_name','Scheme_type']

class scheme_amount_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Scheme_amount_master
        fields=['id','Scheme_name','Scheme_id','Scheme_amount','user_count','status']

class gold_amount_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Gold_master
        fields=['id','Metal_id','Metal_name','Metal_amount','created_on']