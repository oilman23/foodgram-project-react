from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register("users/subscriptions", views.FollowViewSet,
                   basename="Subscriptions",)
router_v1.register("users", views.UserViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
    path("auth/token/login/", obtain_auth_token, name="login"),
    path("auth/token/logout/", views.DeleteToken.as_view(), name="logout")
]
