from django.urls import path
from Receipts.views import *
urlpatterns =[
    path("register",RegisterApi.as_view()),
    path("login",LoginApi.as_view()),
    path("otpsend",OtpSendApi.as_view()),
    path("otpverify",OtpVerifyApi.as_view()),
    path("change/name",ChangeUsernameApi.as_view()),
    path("change/number",PhoneNumberChangeApi.as_view()),
    path("forgot/otp",ResetPasswordOtpApi.as_view()),
    path("forgot/verify",ResetPasswordVerifyApi.as_view()),
    path("forgot/password",ResetPasswordApi.as_view()),
    path("update/password",PasswordUpdateApi.as_view()),
    path("users", UserDetails.as_view()),
    path("create/user", CreateUserApi.as_view()),
]