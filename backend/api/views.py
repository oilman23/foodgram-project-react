import io

from django.db.models import F, Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.permissions import AuthorOrReadOnly

from .mixins import ListRetrieveViewSet
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient, Shopping,
                     Tag)
from .serializers import (IngredientSerializer, RecipeFollowSerializer,
                          RecipeGetSerializer, RecipeSerializer, TagSerializer)
from .utils import delete, post


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("author", "tags",)
    # 'is_favorited', 'is_in_shopping_cart',

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Рецепт успешно удален",
                        status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action != "create":
            return (AuthorOrReadOnly(),)
        return super().get_permissions()

    @action(detail=True, methods=["post", "delete"],)
    def favorite(self, request, pk):
        if self.request.method == "POST":
            return post(request, pk, Favorite, RecipeFollowSerializer)
        return delete(request, pk, Favorite)

    @action(detail=True, methods=["post", "delete"],)
    def shopping_cart(self, request, pk):
        if request.method == "POST":
            return post(request, pk, Shopping, RecipeFollowSerializer)
        return delete(request, pk, Shopping)


class ShoppingCardView(APIView):

    def get(self, request):
        user = request.user
        shopping_list = RecipeIngredient.objects.filter(
            recipe__shopping__user=user).values(
            name=F("ingredient__name"),
            unit=F("ingredient__measurement_unit")
        ).annotate(amount=Sum("amount"))
        font = "DejaVuSerif"
        pdfmetrics.registerFont(
            TTFont("DejaVuSerif", "DejaVuSerif.ttf", "UTF-8")
        )
        buffer = io.BytesIO()
        pdf_file = canvas.Canvas(buffer)
        pdf_file.setFont(font, 24)
        pdf_file.drawString(
            150,
            800,
            "Список покупок."
        )
        pdf_file.setFont(font, 14)
        from_bottom = 750
        for number, ingredient in enumerate(shopping_list, start=1):
            pdf_file.drawString(
                50,
                from_bottom,
                f'{number}.  {ingredient["name"]} - {ingredient["amount"]} '
                f'{ingredient["unit"]}'
            )
            from_bottom -= 20
            if from_bottom <= 50:
                from_bottom = 800
                pdf_file.showPage()
                pdf_file.setFont(font, 14)
        pdf_file.showPage()
        pdf_file.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename="shopping_list.pdf"
        )
