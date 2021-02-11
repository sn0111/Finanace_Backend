from django.urls import path
from Receipts.views import *
urlpatterns =[
    path("register",RegisterApi.as_view()),
    path("login",LoginApi.as_view()),
    path("otpsend",OtpSendApi.as_view()),
    path("otpverify",OtpVerifyApi.as_view()),
]