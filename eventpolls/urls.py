from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "eventpolls"

apiurls = [
    path("events-created/", views.EventListOwner.as_view(), name="event-list-owner"),
    path("events/", views.EventList.as_view(), name="event-list"),
    path("events/<int:event_id>/", views.EventDetail.as_view(), name="event-detail"),
    path(
        "events/<int:event_id>/subscription/",
        views.SubscriptionCreateView.as_view(),
        name="new-subscription",
    ),
    path(
        "unsubscribe/<int:subscription_id>/",
        views.SubscriptionDestroyView.as_view(),
        name="remove-subscription",
    ),
]

urlpatterns = [
    path("api/", include(apiurls)),
    path("", views.index, name="index"),
    path("signup/", views.register_request, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
