from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from core.base_model import BaseModel


class User(AbstractUser, BaseModel):

    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)
    is_seller = models.BooleanField(default=False)

    def full_clean(
        self, exclude = None, validate_unique = True, validate_constraints = True
    ):
        if self.phone and not self.phone.startswith('09'):
            return ValidationError('شماره تلفن وارد شده معتبر نیست.')
        return None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Address(BaseModel):
    label = models.CharField(max_length=11, unique=True, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_address = models.TextField(null=True, blank=True)
    postal_code = models.CharField(max_length=11, unique=True, null=True, blank=True)
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