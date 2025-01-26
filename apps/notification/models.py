from django.db import models
from django.contrib.auth import get_user_model
from council.models import Department

User = get_user_model()


class NOTIFICATION_TYPES:
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    CHOICES = [
        (INFO, "Info"),
        (WARNING, "Warning"),
        (ERROR, "Error"),
    ]


class Notification(models.Model):
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES.CHOICES, default=NOTIFICATION_TYPES.INFO)
    title = models.CharField(max_length=255)
    message = models.TextField()
    class_field = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications"
    )

    # New field for notification history
    notification_history = models.JSONField(
        default=list,
        blank=True,
        help_text="""
        Stores history of sent notifications in format:
        [{
            "id": "uuid",
            "timestamp": "iso-date",
            "status": "sent|delivered|failed",
            "channel": "sms|email|whatsapp",
            "recipient": "user/number/email",
            "error": "error message if failed"
        }]
    """,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.type}: {self.title}"

    def add_to_history(self, status, channel, recipient, error=None):
        """Helper method to add new entry to notification history"""
        from uuid import uuid4
        from datetime import datetime

        entry = {
            "id": str(uuid4()),
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "channel": channel,
            "recipient": recipient,
        }
        if error:
            entry["error"] = error

        if not self.notification_history:
            self.notification_history = []

        self.notification_history.append(entry)
        self.save()


class NotificationSettings(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, related_name="notification_settings")
    enabled = models.BooleanField(default=True)


class MailSettings(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, related_name="mail_settings")
    enabled = models.BooleanField(default=False)


class SmsSettings(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, related_name="sms_settings")
    enabled = models.BooleanField(default=False)


class WhatsappSettings(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, related_name="whatsapp_settings")
    enabled = models.BooleanField(default=False)
