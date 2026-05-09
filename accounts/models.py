import random
from datetime import timedelta
from typing import Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.managers import CustomUserManager
from core.base_model import BaseModel


class User(AbstractUser, BaseModel):

    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True,
                             validators=[RegexValidator(regex=r'^09\d{9}$',)])
    is_seller = models.BooleanField(default=False)

    def make_seller(self) -> bool|None:
        """
        returns True and sets is_seller=True if the user wasn't a seller, otherwise if they
        are already a seller (they have a store) returns None
        """
        if not self.is_seller:
            self.is_seller = True
            self.save()
            return self.is_seller
        return None

    def send_otp(self):
        if not self.phone:
            return None
        # will be replaced with an sms api code
        print(f"OTP code for {self.phone} is {self.otp_code.code}")
        return True


    def get_tokens(self) -> Dict[str, str]:
        """
        Returns a dict that contains access and refresh tokens
        """
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def validate_code(self, code: str) -> bool:
        """
        check if given code is valid for this user
        """
        if self.otp_code and self.otp_code == code:
            return True
        return False

    def save(self, *args,**kwargs):
        super().save(*args, **kwargs)
        otp, created =PhoneOTP.objects.get_or_create(user_id=self.id)
        otp.code = None
        otp.expires_at = None
        otp.save()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class PhoneOTP(BaseModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='otp_code', )
    expires_at = models.DateTimeField(null=True)
    code = models.CharField(null=True)

    def has_expired(self):
        """
        returns True if instane doesn't have an expires_at value,
        or simply checks if expires_at time has passed.
        """
        if not self.expires_at:
            return True
        return self.expires_at < timezone.now()

    def remaining_time(self):
        """
        returns remaining time for otp code in seconds
        """
        if not self.has_expired():
            remaining = self.expires_at - timezone.now()
            return remaining.total_seconds()
        return 0

    def generate_code(self):
        """
        generates a new code if the old one has expired, and sets
        expires_at for 5min later,
        o.w raise exception
        """
        if not self.has_expired():
            raise ValueError(f" ثانیه دوباره تلاش کنید.{self.remaining_time()}لطفا بعد از ")
        otp_code = random.randint(100000, 999999)
        otp_code = str(otp_code)[::-1]
        self.code = otp_code
        self.expires_at = timezone.now() + timedelta(minutes=5)
        self.save()

class Province(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class City(BaseModel):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class Address(BaseModel):
    label = models.CharField(max_length=11, unique=True, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='addresses')
    full_address = models.TextField(null=True, blank=True)
    postal_code = models.CharField(max_length=11, unique=True, null=True, blank=True,
                                   validators=[RegexValidator('^[0-9]{6,}$',
                                                             "کد پستی معتبر نیست.")])
    is_default = models.BooleanField(default=False)

    def save(
        self,
        *args,
        **kwargs,
    ):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} - {self.city}"