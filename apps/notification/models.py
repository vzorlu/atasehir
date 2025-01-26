from django.db import models
from django.contrib.auth import get_user_model

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
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.type}: {self.title}"


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
