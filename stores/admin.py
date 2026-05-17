from django.contrib import admin

from stores.models import Store, Product, Category


# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'address']
    search_fields = ['name', 'address']
    list_filter = ['name']
    list_editable = ['name']
    list_display_links = ['owner']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'stock', 'category']
    search_fields = ['name', 'category__name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']