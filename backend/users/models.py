from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram import settings


class User(AbstractUser):
    ROLES = [
        (settings.ROLE_USER, 'Аутентифицированный пользователь'),
        (settings.ROLE_ADMIN, 'Администратор'),
    ]
    role = models.CharField(
        'Пользовательская роль',
        max_length=16,
        choices=ROLES,
        default='user',
    )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True
    )
    email = models.EmailField('Email', max_length=254, unique=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "author"],
                                    name="unique follow")
        ]

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    # class Meta:
    #     ordering = ('-id',)