from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient, Shopping,
                     Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "text", "cooking_time", "author", "image")
    search_fields = ("name",)
    list_filter = ("cooking_time", "author",)
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "measurement_unit",)
    search_fields = ("name", "measurement_unit",)
    list_filter = ()
    empty_value_display = "-пусто-"


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "id", "ingredient", "amount",)
    search_fields = ("recipe", "ingredient",)
    list_filter = ()
    empty_value_display = "-пусто-"


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "color", "slug",)
    search_fields = ("name",)
    list_filter = ()
    empty_value_display = "-пусто-"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "id", "recipe",)
    search_fields = ("user", "recipe",)
    list_filter = ()
    empty_value_display = "-пусто-"


class ShoppingAdmin(admin.ModelAdmin):
    list_display = ("user", "id", "recipe",)
    search_fields = ("user", "recipe",)
    list_filter = ()
    empty_value_display = "-пусто-"


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Shopping, ShoppingAdmin)
