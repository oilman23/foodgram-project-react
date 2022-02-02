from django.contrib import admin

from .models import Recipe, Ingredient, Quantity, Tag, Favorite, Shopping


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "text", "cooking_time", "author",)
    search_fields = ("name",)
    list_filter = ("cooking_time", "author",)
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "measurement_unit",)
    search_fields = ("name",)
    list_filter = ()
    empty_value_display = "-пусто-"


class QuantityAdmin(admin.ModelAdmin):
    list_display = ("recipe", "id", "ingredient", "value",)
    search_fields = ("recipe", "ingredient",)
    list_filter = ()
    empty_value_display = "-пусто-"


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "color", "slug",)
    search_fields = ("name",)
    list_filter = ()
    empty_value_display = "-пусто-"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "id", "favorite",)
    search_fields = ("user",)
    list_filter = ()
    empty_value_display = "-пусто-"


class ShoppingAdmin(admin.ModelAdmin):
    list_display = ("user", "id", "shopping",)
    search_fields = ("user",)
    list_filter = ()
    empty_value_display = "-пусто-"


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Quantity, QuantityAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Shopping, ShoppingAdmin)
