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


class FinanceOfficeName(models.Model):
    phone_regex = RegexValidator(regex = r'^\+?1?\d{10}$',message = "Phone number must be entered in proper format in 10 digits.")
    choices = (
        (1,"single account"),
        (2,"multiple accounts")
    )
    office_name = models.CharField(max_length=100,blank=True,null=True)
    office_icon = models.ImageField(upload_to='office/')
    office_type = models.CharField(max_length=1,choices=choices)
    address = models.CharField(max_length=200,null=True,blank=True)
    phone_no = models.CharField(max_length=15,validators=[phone_regex])
    pincode = models.IntegerField()
    state = models.CharField(max_length=50,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    # version_id = models.CharField(max_length=30)

    def __str__(self):
        return self.office_name


class Accounts(models.Model):
    account_amount = models.FloatField()
    total_holders = models.CharField(max_length=5)
    required_holders = models.CharField(max_length=5)
    required = models.BooleanField(default=True)
    pause = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    no_of_payments = models.IntegerField()
    # no_of_months = models.IntegerField()
    office = models.ForeignKey(FinanceOfficeName,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.account_amount)


class MonthlyPayment(models.Model):
    payment_no = models.IntegerField()
    bidding_amount = models.FloatField()
    bonus_amount = models.FloatField()
    paid_amount = models.FloatField()
    total_amount = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Accounts,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.payment_no)