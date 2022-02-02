from django.contrib.auth import get_user_model
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.TextField(
        verbose_name="Название ингридиента",
    )
    measurement_unit = models.TextField(
        verbose_name="Единица измерения",
    )

    def __str__(self):
        return self.name[:20]


class Tag(models.Model):
    name = models.TextField(
        max_length=200,
        verbose_name="Название тэга",
    )
    color = models.TextField( # string or null
        max_length=7,
        verbose_name="Цветовой HEX-код",
    )
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    name = models.TextField(
        verbose_name="Название рецепта",
    )
    text = models.TextField(
        verbose_name="Описание рецепта",
    )
    ingredients = models.ManyToManyField(Ingredient, through='Quantity')
    tags = models.ManyToManyField(Tag, verbose_name="Тэг",)
    cooking_time = models.IntegerField(
        verbose_name="Время приготовления в минутах",
    )

    def __str__(self):
        return self.name[:20]
    # image = models.ImageField(
    #     upload_to="posts/", blank=True, null=True,
    #     verbose_name="Картинка поста"
    # )

    # def __str__(self):
    #     return self.text[:15]
    #
    # class Meta:
    #     ordering = ["-pub_date"]


class Quantity(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="amount",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="amount",
    )
    value = models.IntegerField(verbose_name="Количество",)

    # def __str__(self):
    #     return self.value


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_fav"
    )
    favorite = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "favorite"],
                                    name="unique favorite")
        ]


class Shopping(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_cart"
    )
    shopping = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="shopping"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "shopping"],
                                    name="unique shopping")
        ]
