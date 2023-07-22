from django.db import models

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200, null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)


class Attendee(models.Model):
    name = models.CharField(max_length=100, null=False)


class AttendeeToEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, unique=False)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, unique=False)
