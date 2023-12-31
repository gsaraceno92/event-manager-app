from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=200, blank=True)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, unique=False, related_name="attendees"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, unique=False, related_name="subscriptions"
    )
