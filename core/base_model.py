from django.utils import timezone
from django.db import models

from core.base_manager import BaseManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now,db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    objects = BaseManager()

    all_objects = models.Manager()


    class Meta:
        abstract = True
