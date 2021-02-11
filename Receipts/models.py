from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class PhoneOtpVerify(models.Model):
    phone_regex = RegexValidator(regex = r'^\+?1?\d{10}$',message = "Phone number must be entered in proper format in 10 digits.")
    user_phone = models.CharField(max_length=15,validators=[phone_regex])
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    expiry = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.user_phone

