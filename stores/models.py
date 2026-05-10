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


    class Meta:
        ordering = ['name']
        verbose_name_plural = 'stores'


class Category(BaseModel):
    name = models.CharField(max_length=100)


class Product(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    store = models.ManyToManyField(Store, related_name='products', through='StoreItem')
    image = models.ImageField(null=False, blank=False, upload_to='stores/product_images')
    description = models.TextField(null=False, blank=False)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class StoreItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_items')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_items')


class Cart(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='carts')


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    store_item = models.ForeignKey(StoreItem, on_delete=models.CASCADE,
                                   related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)



