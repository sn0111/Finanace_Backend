from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.validators import RegexValidator
# Create your models here.
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, user_phone, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not user_phone:
            raise ValueError(_('The Phone Number must be set'))
        if not password:
            raise ValueError(' User must have a password')
        user = self.model(user_phone=user_phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(user_phone, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    phone_regex = RegexValidator( regex = r'^\+?1?\d{10}$',message = "Phone number must be entered in proper format in 10 digits.")#the format: '+999999999'. Up to 14 digits allowed.")
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100,default=None,blank=True)
    user_phone = models.CharField(max_length=15,validators=[phone_regex],unique=True)
    user_email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "user_phone"
    REQUIRED_FIELDS = []

    objects =UserManager()

    def __str__(self):
        return self.user_phone