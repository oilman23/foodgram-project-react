from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views


router_v1 = DefaultRouter()
router_v1.register('users/subscriptions', views.FollowViewSet,
                   basename='Subscriptions',)
router_v1.register(r"users/<int:id>/", views.UserViewSet)
router_v1.register('users', views.UserViewSet)


urlpatterns = [
    path(r"users/<int:id>/subscribe", views.APISubscribe.as_view()),
    path('', include(router_v1.urls)),
    path('auth/token/login/', obtain_auth_token),

               ]