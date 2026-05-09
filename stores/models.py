from django.db import models
from django.contrib.auth import get_user_model

from core.base_model import BaseModel


# Create your models here.
class Store(BaseModel):
    name = models.CharField(max_length=100)
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='store', unique=True)
    description = models.TextField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.name
