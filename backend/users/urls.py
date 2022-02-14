from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register("users/subscriptions", views.FollowViewSet,
                   basename="Subscriptions",)
router_v1.register("users", views.UserViewSet, basename="Users",)


urlpatterns = [
    path("", include(router_v1.urls)),
    path("auth/token/login/", views.GetTokenAPI.as_view(), name="get_token"),
    path("auth/token/logout/", views.DeleteToken.as_view(), name="logout")
]
