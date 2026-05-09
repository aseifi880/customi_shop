import random
from datetime import timedelta
from typing import Dict

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class PhoneOTP(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp_code')
    expires_at = models.DateTimeField()
    code = models.CharField()

    def has_expired(self):
        return self.expires_at < timezone.now()

    def remaining_time(self):
        if not self.has_expired():
            remaining = self.expires_at - timezone.now()
            return remaining.total_seconds()
        return 0

    def generate_code(self):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
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