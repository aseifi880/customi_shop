from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from core.base_model import BaseModel


class User(AbstractUser, BaseModel):

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True)
    is_seller = models.BooleanField(default=False)

    def full_clean(
        self, exclude = None, validate_unique = True, validate_constraints = True
    ):
        if not self.phone.startswith('09'):
            return ValidationError('شماره تلفن وارد شده معتبر نیست.')
        return None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
