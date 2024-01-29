from django.contrib import admin
from django.utils.html import format_html

from .constants import EXTRA_INGREDIENTS_FIELDS, MINIMUM_REQUIRED
from .models import (Ingredient,
                     Recipe,
                     RecipeIngredient,
                     Tag,
                     FavoriteRecipe,
                     ShoppingCart)


class RecipeIngredientInline(admin.TabularInline):
    """
    Inline admin class for managing recipe ingredients.
    It allows you to edit and add multiple ingredients
    for a recipe on the same page.
    """

    model = RecipeIngredient
    fields = ['ingredient', 'amount', 'measurement_unit']
    readonly_fields = ('measurement_unit',)
    extra = EXTRA_INGREDIENTS_FIELDS
    min_num = MINIMUM_REQUIRED
    empty_value_display = ('Add and save an ingredient first.')

    def measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe Admin for managing recipes in the admin panel."""

    inlines = [RecipeIngredientInline]
    list_filter = ('name', 'author', 'tags')
    list_display = ('name', 'author', 'total_favorites')
    search_fields = ('name', 'author__username')
    search_help_text = 'Search recipe by name or author username'

    @admin.display(description='Total Favorites')
    def total_favorites(self, recipe):
        return recipe.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag Admin for managing tag in the admin panel."""

    list_display = ('name', 'color_tag')

    @admin.display(description='Color')
    def color_tag(self, obj):
        return format_html(
            '<span style="background-color: {0}; color: #fff; padding:'
            '2px 5px; border-radius: 10px;">{0}</span>', obj.color
        )


admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(FavoriteRecipe)
admin.site.register(ShoppingCart)
