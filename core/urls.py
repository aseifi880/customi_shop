
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "کاستومی شاپ"
admin.site.index_title = "مدیریت"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('stores.urls')),
]
