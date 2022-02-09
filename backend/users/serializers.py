from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name",
                  "username", "is_subscribed",)
        read_only_fields = ("id",)

    def get_is_subscribed(self, obj):
        author = self.context["request"].user
        if author.is_anonymous:
            return False
        return obj.follower.filter(author=author).exists()


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128)
    current_password = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = ("new_password", "current_password")
