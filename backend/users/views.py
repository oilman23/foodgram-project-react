from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from .models import User
from api.serializers import FollowSerializer, FollowingSerializer


class CreateDestroyViewSet(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if self.request.method == 'GET':
            data = UserSerializer(self.request.user).data
            return Response(data)


class FollowViewSet(ModelViewSet):
    serializer_class = FollowingSerializer

    def get_queryset(self):
        return self.request.user.following


# class SubscribeViewSet(CreateDestroyViewSet):
#     serializer_class = FollowingSerializer


class APISubscribe(APIView):

    def post(self, request):
        print(request.data)
        serializer = FollowSerializer(data=request.data)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)