from rest_framework import serializers

from accounts.models import User, Address


# region Auth
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "phone", "password")
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
            "phone": {"required": True},
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


# endregion


class UserViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "id",
            "last_login",
            "updated_at",
            "created_at",
            "date_joined",
            "is_superuser",
        )


class UserRetrieveViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "is_seller",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class UserUpdateViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone")


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "label",
            "city",
            "province",
            "full_address",
            "postal_code",
            "created_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
