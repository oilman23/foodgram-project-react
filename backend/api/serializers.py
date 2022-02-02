from django.shortcuts import get_object_or_404
from rest_framework import serializers


from .models import Ingredient, Recipe, Tag, Quantity
from users.serializers import UserSerializer

from users.models import User, Follow


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id',)


class TagPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',)


# class Tag1Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('id',)
#         read_only_fields = ('id',)


class IngredientRecipeGetSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('id', 'name', 'measurement_unit',)

    def get_amount(self, obj):
        return obj.amount.get().value


class IngredientRecipeSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    id = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeGetSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeGetSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text', 'ingredients', 'tags',
                  'cooking_time', 'is_favorited', 'is_in_shopping_cart',)
        read_only_fields = ('id', 'author',)

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if obj.favorite.filter(user=user).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if obj.shopping.filter(user=user).exists():
            return True
        return False


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True)
    author = UserSerializer(read_only=True)
    tags = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=100)
    )

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text', 'ingredients', 'tags',
                  'cooking_time',)
        read_only_fields = ('id', 'author',)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for i in range(len(tags_data)):
            tags = get_object_or_404(Tag, id=tags_data[i])
            recipe.tags.add(tags)
        for i in range(len(ingredients_data)):
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredients_data[i]['id']
            )
            quantity_data = ingredients_data[i]['amount']
            Quantity.objects.create(recipe=recipe, ingredient=ingredient,
                                    value=quantity_data)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        if tags_data:
            instance.tags.clear()
            for i in range(len(tags_data)):
                tags = get_object_or_404(Tag, id=tags_data[i])
                instance.tags.add(tags)
        if ingredients_data:
            amount_set = Quantity.objects.filter(recipe__id=instance.id)
            amount_set.delete()
            for i in range(len(ingredients_data)):
                ingredient = get_object_or_404(
                    Ingredient,
                    id=ingredients_data[i]['id']
                )
                quantity_data = ingredients_data[i]['amount']
                Quantity.objects.create(recipe=instance, ingredient=ingredient,
                                        value=quantity_data)
        instance.save()
        return instance


class RecipeFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time',)
        read_only_fields = ('id',)


class FollowSerializer(serializers.ModelSerializer):
    recipes = RecipeFollowSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'username', 'recipes', 'recipes_count',)
        read_only_fields = ('id',)

    def get_recipes_count(self, obj):
        count = Recipe.objects.filter(author=obj).count()
        return count


class FollowingSerializer(serializers.ModelSerializer):
    user = FollowSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('user',)
        read_only_fields = ()
