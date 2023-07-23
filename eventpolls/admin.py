from django.contrib import admin

from .models import Event, Subscriptions

admin.site.register([Event, Subscriptions])
