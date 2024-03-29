from django.shortcuts import get_object_or_404
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
    ingredients = serializers.SerializerMethodField()
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

    def get_ingredients(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return IngredientRecipeGetSerializer(recipe_ingredients,
                                             many=True).data


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True)
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField(max_length=None, use_url=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = ("id", "author", "name", "text", "ingredients", "tags",
                  "cooking_time", "image")
        read_only_fields = ("id", "author", "tags")

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                ingredient = get_object_or_404(Ingredient, id=ingredient_id)
                raise serializers.ValidationError(
                    f"Ингредиент {ingredient.name} выбран более 1 раза")
            ingredients_list.append(ingredient_id)
        return data

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
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name",
                  "username", "recipes", "recipes_count",)
        read_only_fields = ("id",)

    def get_recipes_count(self, author):
        return Recipe.objects.filter(author=author).count()

    def get_recipes(self, author):
        recipes = author.recipes.all()[:3]
        return RecipeFollowSerializer(recipes, many=True).data
