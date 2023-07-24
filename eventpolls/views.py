import logging
from datetime import date, datetime

import django.contrib.auth as auth
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.messages.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import generics, permissions, response, status
from rest_framework.exceptions import PermissionDenied, ValidationError

from .forms import NewUserForm
from .models import Event, Subscription
from .permissions import IsOwner, IsOwnerOrReadOnly
from .serializers import EventSerializer, SubscriptionSerializer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("views")


def index(request):
    return HttpResponse("Hello. You're at the Events Manager index.")


def login(request):
    request._messages = default_storage(request)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/manager/api/events")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="login.html", context={"login_form": form}
    )


def register_request(request):
    request._messages = default_storage(request)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="register.html",
        context={"register_form": form},
    )


def logout(request):
    if request.method == "POST":
        auth.logout(request)
    return redirect("index")


class EventListOwner(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)


class EventList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    queryset = Event.objects.all().order_by("name")
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def pre_save(self, obj):
        obj.owner = self.request.user


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.owner:
            raise PermissionDenied("Object can not be updated by user.")
        serializer.save()


class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        event_id = self.kwargs.get("event_id")
        event = generics.get_object_or_404(Event, pk=event_id)

        if Subscription.objects.filter(event=event, user=self.request.user).exists():
            return response.Response(
                "User already subscribed to this event.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return response.Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        if datetime.date(event.end_date) <= date.today():
            return response.Response(
                data="Can not create subscriptions for past events.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        event_id = self.kwargs.get("event_id")
        event = generics.get_object_or_404(Event, pk=event_id)

        serializer.save(event=event, user=self.request.user)


class SubscriptionDestroyView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        subscription_id = self.kwargs.get("subscription_id")
        subscription = generics.get_object_or_404(Subscription, pk=subscription_id)
        if subscription.user != self.request.user:
            raise PermissionDenied("Not allowed")

        event = generics.get_object_or_404(Event, pk=subscription.event.id)
        if datetime.date(event.end_date) <= date.today():
            return response.Response(
                data="Can not unregister from subscriptions associated with past events.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
