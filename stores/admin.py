from django.contrib import admin

from stores.models import Store

# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'address']
    search_fields = ['name', 'address']
    list_filter = ['name']
    list_editable = ['name']
    list_display_links = ['owner']
