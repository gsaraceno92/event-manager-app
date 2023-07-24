from datetime import date, datetime

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
            "id",
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

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError(
                "End date should be greater then Start date"
            )

        if datetime.date(end_date) <= date.today():
            raise serializers.ValidationError("End date should be greater then today")

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
