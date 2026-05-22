from django.core.validators import MaxValueValidator
from django.db import models

from accounts.models import User
from core.base_model import BaseModel
from stores.models import Product


# Create your models here.
class ProductComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(null=False, blank=False, max_length=500)
    score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)],
                                        db_comment="score between 0 and 5")

    def __str__(self):
        return f"{self.product.name} - {self.comment}"