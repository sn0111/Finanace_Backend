from rest_framework import serializers
from Receipts.models import *
from res.models import *


class PhoneOtpVerifySerializer(serializers.ModelSerializer):

    class Meta:
        model = PhoneOtpVerify
        fields = ['user_phone']


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_name','user_phone','user_email','password']

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)