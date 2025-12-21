from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone_number", "avatar", "city", "payments"]


class SecureUserData(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "email",
            "avatar",
            "city",
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "avatar", "phone_number", "city", "password"]

    def create(self, validated_data):
        user = User(**validated_data)
        password = validated_data.pop("password")
        user.set_password(password)
        user.save()
        return user
