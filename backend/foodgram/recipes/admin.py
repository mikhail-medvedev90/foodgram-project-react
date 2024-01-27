from django.contrib import admin

from .models import (Ingredient, Recipe, RecipeIngredient, Tag,
                     FavoriteRecipe, ShoppingCart)


class RecipeIngredientInline(admin.TabularInline):
    """
    Inline admin class for managing recipe ingredients.

    This inline class is used within the RecipeAdmin,
    to manage recipe ingredients.

    It allows you to edit and add multiple ingredients
    for a recipe on the same page.
    """

    model = RecipeIngredient
    extra = 5


class RecipeAdmin(admin.ModelAdmin):
    """Recipe Admin for managing recipes in the admin panel."""

    inlines = [RecipeIngredientInline]
    list_filter = ('name', 'author', 'tags')
    list_display = ('name', 'author', 'total_favorites')
    search_fields = ('name', 'author__username')
    search_help_text = 'Search recipe by name or author username'

    def total_favorites(self, obj):
        return obj.favorited_by.count()
    total_favorites.short_description = 'Total Favorites'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Tag)
admin.site.register(FavoriteRecipe)
admin.site.register(ShoppingCart)
