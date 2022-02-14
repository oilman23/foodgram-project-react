from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.pagination import RecipePagination
from api.serializers import FollowSerializer
from .models import Follow, User
from .serializers import GetTokenSerializer, PasswordSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
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
        me = get_object_or_404(User, pk=request.user.pk)
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not me.check_password(serializer.data.get("current_password")):
                return Response({"current_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            me.set_password(serializer.data.get("new_password"))
            me.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    pagination_class = RecipePagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class GetTokenAPI(generics.CreateAPIView):
    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "auth_token": str(token)},
            status=status.HTTP_201_CREATED,
        )


class DeleteToken(APIView):

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)
