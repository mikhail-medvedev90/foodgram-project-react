from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import UserCreateSerializer
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)
from users.models import Subscribe
from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import RecipePagination, UserPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          TagSerializer, UserSerializer, UserSubscriptionList)

User = get_user_model()


class CustomUserCreateView(UserViewSet):
    """
    Custom User creation view with additional actions.
    - me: Retrieve current user's data.
    - subscribe: Subscribe to or unsubscribe from a user.
    - subscriptions: Get a list of user subscriptions.
    """

    serializer_class = UserCreateSerializer
    pagination_class = UserPagination

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        user = self.request.user
        serializer = SubscribeSerializer(
            data={
                'user': user.id,
                'author': author.id
            }, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        subscription = Subscribe.objects.filter(
            user=request.user, author=self.get_object()
        ).first()
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'Subscription not found.'}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        user = request.user
        user_subscriptions = Subscribe.objects.filter(
            user=user
        ).values_list('author')
        authors = User.objects.filter(id__in=user_subscriptions)
        authors_paginated = self.paginate_queryset(authors)
        subscriptions_data = UserSubscriptionList(
            authors_paginated,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(subscriptions_data.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for Tag model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view of the ingredient model with filtering support."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Recipe model.
    - favorite: Add or remove a recipe from favorites.
    - shopping_cart: Add or remove a recipe from the shopping cart.
    - download_shopping_cart: Download the shopping cart as a txt format. file.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    pagination_class = RecipePagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def add_recipe(self, serializer_class, user, pk):
        serializer = serializer_class(
            data={'user': user.id, 'recipe': pk},
            context={'request': self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_recipe(model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        quantity_deleted, _ = model.objects.filter(user=user,
                                                   recipe=recipe).delete()
        if not quantity_deleted:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        return self.add_recipe(FavoriteRecipeSerializer, request.user, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_recipe(FavoriteRecipe, request.user, pk)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        return self.add_recipe(ShoppingCartSerializer, request.user, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_recipe(ShoppingCart, request.user, pk)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        """Method for downloading a shopping list in txt format."""

        user = request.user

        shopping_list = self.generate_shopping_list(user)

        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(
            shopping_list,
            content_type='text/plain; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    def generate_shopping_list(self, user):
        """Generate a list of products that need to be bought."""

        ingredients = RecipeIngredient.objects.filter(
            recipe__cart__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        shopping_list = (f'{user.first_name}, '
                         f'You need to buy the following:\n\n')

        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])

        shopping_list += 'We look forward to seeing you again on our website!'

        return shopping_list
