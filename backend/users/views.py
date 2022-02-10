from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import FollowingSerializer, FollowSerializer

from .models import Follow, User
from .permissions import AuthorOrReadOnly
from .serializers import PasswordSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AuthorOrReadOnly, )
    lookup_field = "id"

    @action(detail=False, methods=["get"],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        data = UserSerializer(self.request.user,
                              context={"request": request}).data
        return Response(data)

    @action(detail=True, methods=["post", "delete"],)
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if self.request.method == "POST":
            if Follow.objects.filter(
                    user=request.user, author=author).exists():
                return Response(
                    {"errors": "Вы уже подписаны на пользователя"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if request.user != author:
                Follow.objects.create(user=request.user, author=author)
                data = FollowSerializer(author,
                                        context={"request": request}).data
                return Response(data)
            return Response({"errors": "Нельзя подписаться на свой аккаунт"},
                            status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=request.user, author=author).exists():
            follow = get_object_or_404(Follow, user=request.user,
                                       author=author)
            follow.delete()
            return Response("Подписка успешно удалена",
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "Вы не подписаны на данного пользователя"},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], )
    def set_password(self, request):
        data = PasswordSerializer(request.data).data
        if data["current_password"] == request.user.password:
            request.user.password = data["new_password"]
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(ModelViewSet):
    serializer_class = FollowingSerializer

    def get_queryset(self):
        return self.request.user.following


class DeleteToken(APIView):

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)
