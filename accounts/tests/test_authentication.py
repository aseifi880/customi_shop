import pytest
from pytest_django.fixtures import django_db_createdb
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate

from accounts.models import User


@pytest.mark.django_db
class TestUserAuthentication:

    def test_anonymous_user_can_register(self):

        data = {
            "email": "random@site.com",
            "password": "password",
            "phone": "09999999999"
        }
        client = APIClient()
        response = client.post("/api/accounts/register/", data=data)

        assert "random@site.com" in response.content.decode('utf-8')
        assert "09999999999" in response.content.decode('utf-8')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1


    def test_anonymous_user_can_login_with_email(self):

        user = User(
            email="random@site.com",
            password="password",
            phone="09999999999")
        user.save()
        client = APIClient()
        response = client.post(
            "/api/accounts/login/", {"email": user.email, "password": user.password} )

        assert response.status_code == status.HTTP_200_OK
        assert "refresh" in response.content.decode('utf-8')
        assert "access" in response.content.decode('utf-8')


    def test_anonymous_user_can_login_with_phone(self):
        user = User(
            phone="09999999999",
            password="password",
            email="random@site.com"
        )
        user.save()

        client = APIClient()
        response_one = client.post("/api/accounts/request-otp/", {"phone": user.phone})
        code = user.otp_code.code
        response_two = client.post("/api/accounts/verify-otp/", {"code": code, "phone": user.phone})

        assert response_one.status_code == status.HTTP_200_OK
        assert "message" in response_one.content.decode('utf-8')
        assert response_two.status_code == status.HTTP_200_OK
        assert "refresh" in response_two.content.decode('utf-8')
        assert "access" in response_two.content.decode('utf-8')