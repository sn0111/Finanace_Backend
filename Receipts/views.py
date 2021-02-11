from django.shortcuts import render
from rest_framework.views import Response,APIView
from rest_framework import generics, permissions
from django.http import HttpResponse
# Create your views here.
from twilio.rest import Client
from res.models import User
from django.contrib.auth import login
from Receipts.models import *
from Receipts.serializer import *
import random
from datetime import datetime, timedelta
from django.utils import timezone
from knox.models import AuthToken
from knox.views import LoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer


account_sid = "AC313b03c0ab2d5e23fef3df4c3f515e41"
auth_token = "82a3b43820272f9bbd144a4c947e9b9e"

client = Client(account_sid,auth_token)
# +16413815187


class OtpSendApi(APIView):

    def post(self,request):
        user_phone = request.data['user_phone']
        user = User.objects.filter(user_phone=user_phone)
        if len(user)>0:
            return Response({"detail":"phone no already exists"})
        phone = PhoneOtpVerify.objects.filter(user_phone=user_phone)
        if len(phone)>0:
            phone.first().delete()
        otp = random.randint(0,999999)
        expiry = timezone.now() + timedelta(minutes=5)
        PhoneOtpVerify.objects.create(user_phone=user_phone,expiry=expiry,otp=otp)
        try:
            client.messages.create(
                to="+91"+user_phone,
                from_="+16413815187",
                body="Verify otp "+str(otp)
            )
        except:
            return Response({'detail':'error occur in sending otp'})
        return Response({'detail':'otp send successfully'})


class OtpVerifyApi(APIView):
    def post(self,request):
        user_phone = request.data['user_phone']
        otp = request.data['otp']
        if user_phone and otp:
            verify = PhoneOtpVerify.objects.filter(user_phone=user_phone).first()
            if verify is None:
                return Response({'detail':'phone no not found'})
            if verify.expiry<timezone.now():
                verify.delete()
                return Response({'detail':'otp session expired'})
            if verify.otp == otp:
                if verify.is_verified==True:
                    return Response({'detail':'otp already verified'})
                verify.is_verified=True
                verify.save()
                return Response({'detail':'otp verified successfully'})
            return Response({'detail':'otp not matched'})
        else:
            return Response({'detail':"some fields missed"})


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        user_phone = request.data['user_phone']
        if user_phone:
            phone = PhoneOtpVerify.objects.filter(user_phone=user_phone).first()
            if phone:
                if phone.is_verified == True:
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response({
                        'detail': 'registered successfully',
                        'token':AuthToken.objects.create(serializer)[1]
                    })
            else:
                return Response({'detail':'you need to verify phone no'})
        return Response({'detail':'registered failed'})


class LoginApi(LoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        response = super(LoginApi, self).post(request,format=None)
        return response
