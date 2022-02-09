from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram import settings


class User(AbstractUser):
    ROLES = [
        (settings.ROLE_USER, "Аутентифицированный пользователь"),
        (settings.ROLE_ADMIN, "Администратор"),
    ]
    role = models.CharField(
        "Пользовательская роль",
        max_length=16,
        choices=ROLES,
        default='user',
    )
    first_name = models.CharField(
        "Имя",
        max_length=150
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150
    )
    username = models.CharField(
        "Логин",
        max_length=150,
        unique=True
    )
    email = models.EmailField("Email", max_length=254, unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower",
                             verbose_name="Подписавшийся")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following",
        verbose_name="Пользователь, на которго подписались"
    )

    class Meta:
        verbose_name = "Подписки"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(fields=["user", "author"],
                                    name="unique follow")
        ]
