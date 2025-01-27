from rest_framework import serializers
from .models import NOTIFICATION_TYPES, Notification, NotificationChannel


class NotificationRuleSerializer(serializers.ModelSerializer):
    channels = serializers.MultipleChoiceField(choices=NOTIFICATION_TYPES.CHOICES)

    class Meta:
        model = Notification
        fields = ["rule_name", "channels", "message", "class_field", "department", "user"]

    def create(self, validated_data):
        channels_data = validated_data.pop("channels")
        notification = Notification.objects.create(**validated_data)

        for channel_type in channels_data:
            channel, _ = NotificationChannel.objects.get_or_create(name=channel_type)
            notification.channels.add(channel)

        return notification


class NotificationSendSerializer(serializers.Serializer):
    class_field = serializers.CharField(required=True)
    data = serializers.JSONField(required=False)  # Additional data for notification
