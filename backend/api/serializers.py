from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer

from .models import Ingredient, Recipe, RecipeIngredient, Tag
from .utils import recipe_ingredient_create


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit",)
        read_only_fields = ("id",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")
        read_only_fields = ("id",)


class IngredientRecipeGetSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount", "name", "measurement_unit")


class IngredientRecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.IntegerField(write_only=True, min_value=1)
    id = serializers.PrimaryKeyRelatedField(
        source="ingredient",
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount", "recipe")


class RecipeGetSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientRecipeGetSerializer(source="recipe_ingredient",
                                                many=True, read_only=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("id", "author", "name", "text", "ingredients", "tags",
                  "cooking_time", "is_favorited", "is_in_shopping_cart",
                  "image")
        read_only_fields = ("id", "author",)

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.favorite.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.shopping.filter(user=user).exists()


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True)
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ("id", "author", "name", "text", "ingredients", "tags",
                  "cooking_time", "image")
        read_only_fields = ("id", "author", "tags")

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags_data = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        recipe_ingredient_create(ingredients_data, RecipeIngredient, recipe)
        return recipe

    def update(self, instance, validated_data):
        if "tags" in self.validated_data:
            tags_data = validated_data.pop("tags")
            instance.tags.set(tags_data)
        if "ingredients" in self.validated_data:
            ingredients_data = validated_data.pop("ingredients")
            amount_set = RecipeIngredient.objects.filter(
                recipe__id=instance.id)
            amount_set.delete()
            recipe_ingredient_create(ingredients_data, RecipeIngredient,
                                     instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        self.fields.pop("ingredients")
        self.fields.pop("tags")
        representation = super().to_representation(instance)
        representation["ingredients"] = IngredientRecipeGetSerializer(
            RecipeIngredient.objects.filter(recipe=instance), many=True
        ).data
        representation["tags"] = TagSerializer(
            instance.tags, many=True
        ).data
        return representation


class RecipeFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time",)
        read_only_fields = ("id",)


class FollowSerializer(serializers.ModelSerializer):
    recipes = RecipeFollowSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name",
                  "username", "recipes", "recipes_count",)
        read_only_fields = ("id",)

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
