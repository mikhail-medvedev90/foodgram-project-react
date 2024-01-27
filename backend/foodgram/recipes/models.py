from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()
HexColorRegexPattern = r'#([A-Fa-f0-9]{6})|#([A-Fa-f0-9]{3})|#([A-Fa-f0-9]{8})'


class Tag(models.Model):
    """Tag model."""

    name = models.CharField(
        _('Name'),
        unique=True,
        max_length=200,
    )
    color = models.CharField(
        _('Color value in hex format'),
        unique=True,
        max_length=9,
        help_text=_('Input color value in hex format starting with #.'),
        validators=(
            RegexValidator(
                regex=HexColorRegexPattern,
                message=_(
                    'Enter a valid hex color code. Example: #000000. '
                    'Hint: HEX color in short format and with alpha channel '
                    'is also supported.'
                )
            ),
        ),
    )
    slug = models.SlugField(
        _('Slug'),
        unique=True,
        max_length=200,
        error_messages={
            'unique': _('Please, try another one. All slugs must be unique.'),
        },
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Recipe model."""

    tags = models.ManyToManyField(
        'Tag',
        related_name='recipe',
        verbose_name=_('Tags'),
    )
    author = models.ForeignKey(
        User,
        related_name='recipe',
        verbose_name=_('Author'),
        on_delete=models.CASCADE,
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='ingredient',
        verbose_name=_('Ingredients'),
    )
    name = models.CharField(
        _('Name'),
        max_length=200,
    )
    image = models.ImageField(
        _('Image'),
        upload_to='recipes/',
    )
    text = models.TextField(
        _('Text'),
    )
    cooking_time = models.PositiveIntegerField(
        _('Cooking time'),
        help_text=_('Input the total cooking time in minutes.'),
        validators=[
            MinValueValidator(
                1,
                message=_('Cooking time must be at least 1 minute.'),
            ),
        ],
    )
    pub_date = models.DateTimeField(
        _('Publication Date'),
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Ingredient model."""

    name = models.CharField(
        _('Name'),
        max_length=200,
    )
    measurement_unit = models.CharField(
        _('Measurement unit'),
        max_length=200,
    )

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    """Intermediate model to represent ingredients in a recipe."""

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name=_('Recipe'),
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name=_('Ingredient'),
    )
    amount = models.PositiveIntegerField(
        _('Amount'),
        default=1,
        validators=(
            MinValueValidator(
                1,
                message='Amount must be at least 1.',
            ),
        ),
    )

    class Meta:
        verbose_name = _('Recipe ingredient')
        verbose_name_plural = _('Recipe ingredients')

    def __str__(self) -> str:
        return (
            f'{self.ingredient.name}: '
            f'{self.amount} {self.ingredient.measurement_unit}.'
        )


class ShoppingCart(models.Model):
    """Shopping cart model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_('Recipe'),
        related_name='cart'
    )

    class Meta:
        verbose_name = _('Shopping cart')
        verbose_name_plural = _('Shopping carts')
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            ),
        )

    def __str__(self) -> str:
        return f'Корзина пользователя {self.user.username}'


class FavoriteRecipe(models.Model):
    """Model for favorite recipes."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='favorited_by'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_('Recipe'),
        related_name='favorited_by'
    )

    class Meta:
        verbose_name = _('Favorite Recipe')
        verbose_name_plural = _('Favorite Recipes')
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe'
            ),
        )

    def __str__(self) -> str:
        return self.recipe.name
