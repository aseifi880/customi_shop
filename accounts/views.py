from django.core.serializers import serialize
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from stores.models import Store
from stores.serializers import StoreSerializer
from .models import User, Address
from .serializers import RegisterSerializer, LoginSerializer, RequestOTPSerializer, VerifyOTPSerializer, \
    UserRetrieveViewSerializer, UserUpdateViewSerializer, UserAddressSerializer


class RegisterView(APIView):
    """
    Register a new user using either email, phone or both.
    if both, user can log in by `register/` or `request-otp/`,
    if only email or phone, log in from `register/` or `request-otp/` respectively.
    """
    def post(self, request: Request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
        # credential validation happens inside the manager and model.
            user = User.objects.create_user(**serializer.validated_data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not user:
            return Response({
                "error": "مقادیر وارد شده قابل قبول نیست.",
            }, status=status.HTTP_400_BAD_REQUEST)


        return Response({
            "message": "کاربر با موفقیت ایجاد شد.",
            "data": {
                "email": user.email,
                "phone": user.phone,
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    """
    I am assuming that login url is only for log in
    with email and password.
    """
    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data['email'])
        if not user:
            return Response({
                "error": "اطلاعات داده شده صحیح نمی باشد."
            }, status=status.HTTP_400_BAD_REQUEST)

        tokens = user.get_tokens()
        return Response(tokens, status=status.HTTP_200_OK)


class RequestOTPView(APIView):

    """
    If phone was given on sign up, user can request otp code then verify it o.w.
    they will receive an error as this route does not create a new user.
    """
    def post(self, request: Request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']
        user = User.objects.get(phone=phone)

        if not user.check_password(password):
            return Response({
                "error": "اطلاعات وارد شده صحیح نمی باشد."
            }, status=status.HTTP_400_BAD_REQUEST)

        user.otp_code.generate_code()
        user.send_otp()
        return Response({
            "message": "کد یکبار مصرف ارسال شد."
        }, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request: Request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        user = User.objects.get(phone=phone)
        if is_valid := user.validate_code(code):
            tokens = user.get_tokens()
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({
            "error": "کد وارد شده صحیح نمیباشد."
        }, status=status.HTTP_400_BAD_REQUEST)


class UserView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserRetrieveViewSerializer
        return UserUpdateViewSerializer


class UserAddressViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterAsSellerView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request):
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        is_made_seller = user.make_seller()

        if not is_made_seller:
            return Response({
                "error": "کاربر در حال حاضر فروشنده است."
            }, status=status.HTTP_400_BAD_REQUEST)

        store = Store.objects.create(
            user=user,
            name=serializer.validated_data['name'],
            address=serializer.validated_data['address'],
            description=serializer.validated_data['description'],
        )

        return Response({
            "message": "کاربر با موفقیت تبدیل به فروشنده شد.",
            "data": StoreSerializer(store).data
        })


