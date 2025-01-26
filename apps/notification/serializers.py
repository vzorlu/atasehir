from rest_framework import serializers
from .models import Notification


class NotificationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["type", "title", "message", "class_field", "department", "user"]
