from django.contrib.auth import get_user_model
from django.db.models import F
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .mixins import IsSubscribedMixin
from users.models import Subscribe
from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """User creation serializer based on Djoser UserCreateSerializer."""


class UserSerializer(IsSubscribedMixin, serializers.ModelSerializer):
    """
    Serializer for the User model with subscription information.

    Provides information about users and their subscription status.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class UserSubscriptionList(IsSubscribedMixin, serializers.Serializer):
    """
    Serializer for User model with subscription list and recipe count.

    Retrieves data about users, their subscription list, and recipe counts.
    """

    id = serializers.IntegerField()

    def get_author_recipes(self, user):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=user)

        if recipes_limit is not None:
            recipes_limit = int(recipes_limit)
            recipes = Recipe.objects.filter(author=user)[:recipes_limit]

        recipe_serializer = RecipeShortSerializer(recipes, many=True)
        return recipe_serializer.data

    def get_author_recipes_count(self, user):
        return Recipe.objects.filter(author=user).count()

    def to_representation(self, instance):
        author_data = UserSerializer(instance).data

        return {
            **author_data,
            'is_subscribed': self.get_is_subscribed(instance),
            'recipes': self.get_author_recipes(instance),
            'recipes_count': self.get_author_recipes_count(instance)
        }


class SubscribeSerializer(UserSubscriptionList):
    """
    Serializer for subscribing to another user.

    Handles user subscriptions with custom error messages.
    """

    default_error_messages = {
        'subscribe_to_self': 'You cannot subscribe to yourself.',
        'already_subscribed': 'You are already subscribed to this user.',
    }

    def create(self, validated_data):
        user = self.context['request'].user
        author_id = validated_data['id']

        if user.id == author_id:
            self.fail('subscribe_to_self')

        if Subscribe.objects.filter(
            user_id=user.id,
            author_id=author_id
        ).exists():
            self.fail('already_subscribed')

        author = get_object_or_404(User, id=author_id)
        Subscribe.objects.create(user=user, author=author)
        return author


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model.

    Provides Tag model serialization for listing and detail views.
    """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ingredient model.

    Provides Ingredient model serialization for listing and detail views.
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Recipe details with additional information.

    Serializes Recipe model for reading, including ingredients, favorites,
    and shopping cart status.
    """

    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipeingredient__amount')
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return FavoriteRecipe.objects.filter(
                user=user,
                recipe=obj
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return ShoppingCart.objects.filter(
                user=user,
                recipe=obj
            ).exists()
        return False


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for writing Recipe Ingredient details.

    Serializes Recipe Ingredient for writing details, including id, amount,
    name, and measurement unit.
    """

    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(required=True)
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', 'name', 'measurement_unit')

    def get_measurement_unit(self, ingredient):
        return ingredient.measurement_unit

    def get_name(self, ingredient):
        return ingredient.name


class RecipeWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for writing Recipe details with validation.

    Handles the creation and updating of recipes with custom error messages.

    Serializes Recipe model for writing and updating, including tags,
    ingredients, image, name, text, and cooking time.
    """

    default_error_messages = {
        'unique_ingredients': 'Ingredients of the recipe must be unique',
        'invalid_amount': 'Invalid ingredient amount',
        'unique_tags': 'Recipe tags must be unique',
        'no_ingredients': 'Recipe must contain at least 1 ingredient',
        'no_tags': 'Recipe must contain at least 1 tag',
        'ingredients_doesnt_exist': 'This ingredient does not exist in db',
        'no_image': 'Image is required',
        'incorrect_tag': 'Incorrect tag is provided.',
    }

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = RecipeIngredientWriteSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )
        read_only_fields = ('author',)

    def validate_image(self, image):
        if not image:
            self.fail('no_image')

    def validate_ingredients(self, ingredients):
        if not ingredients:
            self.fail('no_ingredients')
        ingredients_data = [
            ingredient.get('id') for ingredient in ingredients
        ]
        for ingredient_id in ingredients_data:
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                self.fail('ingredients_doesnt_exist')

        if len(ingredients_data) != len(set(ingredients_data)):
            self.fail('unique_ingredients')
        for ingredient in ingredients:
            if int(ingredient.get('amount')) < 1:
                self.fail('invalid_amount')
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            self.fail('no_tags')
        if len(tags) != len(set(tags)):
            self.fail('unique_tags')
        return tags

    def add_ingredients(self, ingredients_data, recipe):
        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient_data.get('id'),
                amount=ingredient_data.get('amount')
            )
            for ingredient_data in ingredients_data
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        recipe.save()
        self.add_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.name)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.tags.clear()
        instance.ingredients.clear()

        tags_data = validated_data.get('tags')
        self.validate_tags(tags_data)
        instance.tags.set(tags_data)

        ingredients_data = validated_data.get('ingredients')
        self.validate_ingredients(ingredients_data)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.add_ingredients(ingredients_data, instance)

        instance.save()
        return instance

    def to_representation(self, recipe):
        serializer = RecipeReadSerializer(recipe)
        return serializer.data


class RecipeShortSerializer(serializers.ModelSerializer):
    """
    Serializer for Recipe with minimal details.

    Provides minimal details for Recipe model, including id, name,
    image, and cooking time.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
