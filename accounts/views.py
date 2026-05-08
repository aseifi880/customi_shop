from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, RequestOTPSerializer


class RegisterView(APIView):

    def post(self, request: Request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.get(email=email)

        if user:
            return Response("مقادیر وارد شده قابل قبول نیست.", status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.create_user(email=email, password=password)
        except ValueError as e:
            return Response({
                'error': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "کاربر با موفقیت ایجاد شد.",
            "email": email,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data['email'])
        tokens = user.get_tokens()
        return Response(tokens, status=status.HTTP_200_OK)


class RequestOTPView(APIView):
    def post(self, request: Request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']
        user = User.objects.get(phone=phone)

        if user.check_password(password):
            user.otp_code.generate_code()
            print(f"Your OTP code is {user.otp_code.code}")
            return Response({
                "message": "کد یکبار مصرف ارسال شد."
            })

        return Response({
            "message": "اطلاعات وارد شده صحیح نمی باشد."
        }, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request: Request):
        pass