import django.contrib.auth as auth
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.messages.storage import default_storage
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import generics, permissions, response, status

from .forms import NewUserForm
from .models import Event, Subscription
from .permissions import IsOwner, IsOwnerOrReadOnly
from .serializers import EventSerializer, SubscriptionSerializer


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

    def perform_create(self, serializer):
        event_id = self.kwargs.get("event_id")
        event = generics.get_object_or_404(Event, pk=event_id)

        if Subscription.objects.filter(event=event, user=self.request.user).exists():
            raise PermissionDenied("User already present", status.HTTP_400_BAD_REQUEST)

        serializer.save(event=event, user=self.request.user)

    def pre_save(self, obj):
        obj.event = self.kwargs.get("event_id")
        obj.user = self.request.user


class SubscriptionDestroyView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        subscription_id = self.kwargs.get("subscription_id")
        subscription = generics.get_object_or_404(Subscription, pk=subscription_id)

        if subscription.user != self.request.user:
            raise PermissionDenied("Not allowd")

        subscription.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
