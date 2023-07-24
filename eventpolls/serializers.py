from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Event, Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Subscription
        fields = ["id", "user"]


class EventSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "name",
            "description",
            "start_date",
            "end_date",
            "owner",
            "subscriptions",
        )

    def get_subscriptions(self, obj):
        subscriptions = Subscription.objects.filter(event=obj)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
