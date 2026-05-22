from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()
router.register(
    "myuser/address", views.UserAddressViewSet, basename="current-user-address"
)
router.register("admin/users", views.UserViewSet, basename="admin-users")


urlpatterns = [
    path("accounts/register/", views.RegisterView.as_view(), name="register"),
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path("accounts/request-otp/", views.RequestOTPView.as_view(), name="request-otp"),
    path("accounts/verify-otp/", views.VerifyOTPView.as_view(), name="verify_otp"),
    path("accounts/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("myuser/", views.UserView.as_view(), name="user"),
    path(
        "myuser/register_as_seller/",
        views.RegisterAsSellerView.as_view(),
        name="register_as_seller",
    ),
]
urlpatterns += router.urls
