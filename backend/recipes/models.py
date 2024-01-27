from django.contrib.auth import get_user_model
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    RegexValidator)
from django.db import models

User = get_user_model()

hex_regex_pattern = r'#([A-Fa-f0-9]{6})|#([A-Fa-f0-9]{3})|#([A-Fa-f0-9]{8})'

DEFAULT_FIELD_LENGHT = 200
MIN_VALUE_REQUIRED = 1
MAX_VALUE_LIMIT = 1440


class Tag(models.Model):
    """Tag model."""

    name = models.CharField(
        'Name',
        unique=True,
        max_length=DEFAULT_FIELD_LENGHT,
    )
    color = models.CharField(
        'Color value in hex format',
        unique=True,
        max_length=9,
        help_text='Input color value in hex format starting with #.',
        validators=(
            RegexValidator(
                regex=hex_regex_pattern,
                message=(
                    'Enter a valid hex color code. Example: #000000. '
                    'Hint: HEX color in short format and with alpha channel '
                    'is also supported.'
                )
            ),
        ),
    )
    slug = models.SlugField(
        'Slug',
        unique=True,
        max_length=DEFAULT_FIELD_LENGHT,
        error_messages={
            'unique': 'Please, try another one. All slugs must be unique.',
        },
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Recipe model."""

    tags = models.ManyToManyField(
        'Tag',
        related_name='recipe',
        verbose_name='Tags',
    )
    author = models.ForeignKey(
        User,
        related_name='recipe',
        verbose_name='Author',
        on_delete=models.CASCADE,
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='ingredient',
        verbose_name='Ingredients',
    )
    name = models.CharField(
        'Name',
        max_length=DEFAULT_FIELD_LENGHT,
    )
    image = models.ImageField(
        'Image',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Text',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Cooking time',
        help_text='Input the total cooking time in minutes.',
        validators=[
            MinValueValidator(
                MIN_VALUE_REQUIRED,
                message='Cooking time must be at least 1 minute.',
            ),
            MaxValueValidator(
                MAX_VALUE_LIMIT,
                message='Cooking time cannot be greater than 1440 (24hours)'
            ),
        ],
    )
    pub_date = models.DateTimeField(
        'Publication Date',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Ingredient model."""

    name = models.CharField(
        'Name',
        max_length=DEFAULT_FIELD_LENGHT,
    )
    measurement_unit = models.CharField(
        'Measurement unit',
        max_length=DEFAULT_FIELD_LENGHT,
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    """Model to ingredients in a recipe."""

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Recipe',
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name='Ingredient',
    )
    amount = models.PositiveSmallIntegerField(
        'Amount',
        default=1,
        validators=(
            MinValueValidator(
                MIN_VALUE_REQUIRED,
                message='Amount must be at least 1.',
            ),
            MaxValueValidator(
                MAX_VALUE_LIMIT,
                message='Amount must be at most 1111.',
            )
        ),
    )

    class Meta:
        verbose_name = 'Recipe ingredient'
        verbose_name_plural = 'Recipe ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self) -> str:
        return (
            f'{self.ingredient.name}: '
            f'{self.amount} {self.ingredient.measurement_unit}.'
        )


class FavoriteRecipeShoppingCartRelation(models.Model):
    """
    Abstract model for user relations.
    For ShoppingCart and FavoriteRecipe models.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe',
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.recipe.name


class ShoppingCart(FavoriteRecipeShoppingCartRelation):
    """Shopping cart model."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='check_shopping_cart_unique'
            )
        ]
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts'
        default_related_name = 'cart'


class FavoriteRecipe(FavoriteRecipeShoppingCartRelation):
    """Favorite recipe model."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='check_favorite_unique'
            )
        ]
        verbose_name = 'Favorite Recipe'
        verbose_name_plural = 'Favorite Recipes'
        default_related_name = 'favorites'
