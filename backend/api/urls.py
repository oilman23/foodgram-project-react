from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, ShoppingCardView,
                    TagViewSet)

router_v1 = DefaultRouter()
router_v1.register("ingredients", IngredientViewSet)

router_v1.register("recipes", RecipeViewSet)
router_v1.register("tags", TagViewSet)

urlpatterns = [
    path("recipes/download_shopping_cart/", ShoppingCardView.as_view(),
         name="download_shopping_cart"),
    path("", include(router_v1.urls)),
]
