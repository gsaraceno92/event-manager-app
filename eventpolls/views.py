import django.contrib.auth as auth
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.messages.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import viewsets

from .forms import NewUserForm
from .models import Event
from .serializers import EventSerializer


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
                return redirect("index")
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


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("name")
    serializer_class = EventSerializer
