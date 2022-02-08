from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, \
    ShoppingCardView

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientViewSet)

router_v1.register('recipes', RecipeViewSet)
router_v1.register('tags', TagViewSet)

urlpatterns = [
    path(f'recipes/download_shopping_cart/', ShoppingCardView.as_view()),
    path('', include(router_v1.urls)),
               ]
