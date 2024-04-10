from chit.models import User_Management
from rest_framework import serializers


class User_Serializer(serializers.ModelSerializer):

    class Meta:
        model = User_Management
    fields=['user_name','Email','mobile_number']