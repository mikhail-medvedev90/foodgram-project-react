from django.contrib.auth import get_user_model
from django_filters import FilterSet
from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag

User = get_user_model()


class RecipeFilter(FilterSet):
    """Custom filter for recipes."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
        label='Is in shopping cart'
    )

    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited',
        label='Is favorited'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value:
                return queryset.filter(cart__user=self.request.user)
            return queryset.exclude(cart__user=self.request.user)
        return queryset.none()

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value:
                return queryset.filter(favorited_by__user=self.request.user)
            return queryset.exclude(favorited_by__user=self.request.user)
        return queryset.none()
