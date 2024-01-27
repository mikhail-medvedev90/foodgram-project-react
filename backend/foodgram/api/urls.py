from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (CustomUserCreateView, IngredientViewSet, RecipeViewSet,
                    TagViewSet)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'tags', TagViewSet)
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'ingredients', IngredientViewSet)
router_v1.register(r'users', CustomUserCreateView)

urlpatterns = [
    path('', include(router_v1.urls)),
]

djoserurls = [
    path('', include('djoser.urls'),),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += djoserurls
