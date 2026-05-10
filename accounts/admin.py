from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.models import Address, City, PhoneOTP, Province

User = get_user_model()

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone','first_name',
                    'last_name', 'is_staff', 'is_active',
                    'date_joined',
                    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'label', 'city', 'province', 'full_address', 'user'
    )

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('province', 'name')

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)

