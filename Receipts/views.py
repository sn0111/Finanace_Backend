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
            # phone = PhoneOtpVerify.objects.filter(user_phone=user_phone).first()
            # if phone:
            #     if phone.is_verified == True:
            #         serializer = self.get_serializer(data=request.data)
            #         serializer.is_valid(raise_exception=True)
            #         user=serializer.save()
            #         return Response({
            #             'detail': 'registered successfully',
            #             'token':AuthToken.objects.create(user)[1]
            #         })
            # else:
            #     return Response({'detail':'you need to verify phone no'})
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user=serializer.save()
            return Response({
                'detail': 'registered successfully',
                'token': AuthToken.objects.create(user)[1]
            })
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


class ChangeUsernameApi(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self,request):
        user_name = request.data['user_name']
        if user_name:
            try:
                user=User.objects.get(user_phone=request.user.user_phone)
                user.user_name = user_name
                user.save()
                return Response(data="name changes successfully")
            except:
                return Response(data="error occured")
        else:
            return Response(data="missed username")


class PhoneNumberChangeApi(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self,request):
        user_phone = request.data['user_phone']
        otp = request.data['otp']
        if user_phone and otp:
            phone = PhoneOtpVerify.objects.filter(user_phone=user_phone).first()
            if phone:
                if phone.expiry<timezone.now():
                    phone.delete()
                    return Response(data="session expired")
                if phone.otp!=otp:
                    return Response(data="otp not matched")
                if phone.is_verified==True:
                    return Response(data="Already updated")
                phone.is_verified=True
                phone.save()
                user=User.objects.filter(user_phone=request.user.user_phone)
                user.user_phone=user_phone
                user.save()
                return Response(data="phone number has changed successfully")
            else:
                return Response(data="otp not sent")
        else:
            return Response(data="missed some fields")


class ResetPasswordOtpApi(APIView):

    def post(self,request):
        user_phone = request.data['user_phone']
        user = User.objects.filter(user_phone=user_phone).first()
        if user:
            phone = PhoneOtpVerify.objects.filter(user_phone=user_phone)
            if len(phone)>0:
                phone.delete()
            otp = random.randint(0,999999)
            expiry = timezone.now()+timedelta(minutes=5)
            PhoneOtpVerify.objects.create(user_phone=user_phone,otp=otp,expiry=expiry)
            try:
                client.messages.create(
                    to="+91" + user_phone,
                    from_="+16413815187",
                    body="Verify otp " + str(otp)
                )
            except:
                return Response({'detail': 'error occur in sending otp'})
        return Response(data="phone number not exists")


class ResetPasswordVerifyApi(APIView):

    def post(self,request):
        user_phone = request.data['user_phone']
        otp = request.data['otp']
        if user_phone and otp:
            phone = PhoneOtpVerify.objects.filter(user_phone=user_phone)
            if len(phone)>0:
                phone = phone.first()
                if phone.expiry<timezone.now():
                    phone.delete()
                    return Response(data="session expired")
                if phone.otp == otp:
                    if phone.is_verified==True:
                        return Response(data="otp verified already")
                    phone.is_verified=True
                    phone.save()
                    return Response(data="otp verified success")
            return Response(data="otp not sent")
        return Response(data="missed fields")


class ResetPasswordApi(APIView):

    def post(self,request):
        user_phone = request.data['user_phone']
        if user_phone:
            phone = PhoneOtpVerify.objects.filter(user_phone=user_phone).first()
            if phone:
                if phone.is_verified==True:
                    return Response(data="phone number not verified")
            else:
                return Response(data="phone number verified")
            try:
                user = User.objects.get(user_phone=user_phone)
                user.set_password(request.data['password'])
                user.save()
                return Response(data="password reset success")
            except:
                return Response(data="error occured")


class PasswordUpdateApi(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self,request):
        old_password=request.data['old_password']
        new_password=request.data['new_password']
        if old_password and new_password:
            try:
                user = User.objects.get(user_phone=request.user.user_phone)
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    return Response(data="password updated successfully")
                else:
                    return Response(data="old password incorrect")
            except:
                return Response(data="error occured")
        else:
            return Response(data="missed some fields")


class CreateUserApi(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self,request):
        user = User.objects.create_superuser(
            user_phone=request.data['user_phone'],
            user_name=request.data['user_name'],
            user_email=request.data.get('user_email'),
            designation= request.data['designation'],
            is_staff=True,
            employee_id=request.data.get('employee_id'),
            password="1234"
        )
        return Response(data="User created Successfully")


class UserDetails(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        query = User.objects.all()
        return query
