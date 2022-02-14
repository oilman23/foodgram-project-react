from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "password", "email", "first_name", "last_name",
                  "username", "is_subscribed",)
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128)
    current_password = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = ("new_password", "current_password")


class GetTokenSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, data):
        email_request = data.get("email")
        user = User.objects.filter(email=email_request)

        if not user.exists():
            raise serializers.ValidationError({
                "email": "Неверно указан адрес электронной почты"
            })

        if not get_object_or_404(
                User, email=email_request
        ).check_password(data.get("password")):
            raise serializers.ValidationError({
                "password": "Введен неверный пароль."
            })
        return user.get()
