from rest_framework import serializers

from accounts.models import User, Address, Province, City


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'phone','password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': False},
            'phone': {'required': False}
                        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, required=True)
    password = serializers.CharField(write_only=True, required=True)


class VerifyOTPSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)
    phone = serializers.CharField(max_length=11)


class UserRetrieveViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'is_seller','created_at', 'updated_at')
        read_only_fields = fields

class UserUpdateViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
