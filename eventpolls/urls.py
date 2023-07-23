from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"events", views.EventsViewSet)


apiurls = [
    path("api/", include(router.urls)),
]

urlpatterns = [
    *apiurls,
    path("", views.index, name="index"),
    path("signup/", views.register_request, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
