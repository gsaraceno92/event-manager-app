from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"events", views.EventsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", views.index, name="index"),
    path("signup/", views.register_request, name="signup"),
    path("login/", views.login, name="login"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
