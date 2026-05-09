from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("request-otp/", views.RequestOTPView.as_view(), name="request-otp"),
    path("verify-otp/", views.VerifyOTPView.as_view(), name="verify_otp"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('myuser/', views.UserView.as_view(), name='user'),
    path('myuser/address/', views.UserAddressView.as_view(), name='user_address'),
    path('myuser/register_as_seller/', views.RegisterAsSellerView.as_view(), name='register_as_seller'),

]