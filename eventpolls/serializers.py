from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Event
        fields = ("name", "description", "start_date", "end_date", "owner")
