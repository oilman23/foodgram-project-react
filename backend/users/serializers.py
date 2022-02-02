from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'username', 'is_subscribed',)
        read_only_fields = ('id',)

    def get_is_subscribed(self, obj):
        author = self.context['request'].user
        if obj.follower.filter(author=author).exists():
            return True
        return False
