from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.TextField(
        verbose_name="Название ингридиента",
    )
    measurement_unit = models.TextField(
        verbose_name="Единица измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name[:20]


class Tag(models.Model):
    name = models.TextField(
        max_length=200,
        verbose_name="Название тэга",
    )
    color = models.TextField(
        max_length=7,
        verbose_name="Цветовой HEX-код",
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name="Slug тэга",
        unique=True,
        db_index=True)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes",
                               verbose_name="Автор рецепта",)
    name = models.TextField(verbose_name="Название рецепта",)
    text = models.TextField(verbose_name="Описание рецепта",)
    image = models.ImageField(upload_to="recipes/",
                              verbose_name="Фотография рецепта")
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name="Ингредиенты рецепта",
                                         through="RecipeIngredient",)
    tags = models.ManyToManyField(Tag, verbose_name="Тэги рецепта",)
    cooking_time = models.IntegerField(
        verbose_name="Время приготовления в минутах",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name[:20]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="amount",
        verbose_name="Рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="amount",
        verbose_name="Ингредиент"
    )
    amount = models.IntegerField(verbose_name="Количество",)

    class Meta:
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количество ингредиента"
        constraints = [
            models.UniqueConstraint(fields=["recipe", "ingredient"],
                                    name="unique_recipe_ingredient")
        ]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_fav",
                             verbose_name="Автор списка избранного")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="favorite",
                               verbose_name="Рецепт из списка избранного")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"],
                                    name="unique favorite")
        ]


class Shopping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_cart",
                             verbose_name="Автор списка покупок")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="shopping",
                               verbose_name="Рецепт из списка покупок")

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"],
                                    name="unique shopping")
        ]
