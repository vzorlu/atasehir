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


class NotificationSettings(models.Model):
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MailSettings(NotificationSettings):
    notification = models.OneToOneField("Notification", on_delete=models.CASCADE, related_name="mail_settings")
    email_template = models.TextField(null=True, blank=True)


class SmsSettings(NotificationSettings):
    notification = models.OneToOneField("Notification", on_delete=models.CASCADE, related_name="sms_settings")
    sms_template = models.TextField(null=True, blank=True)


class WhatsappSettings(NotificationSettings):
    notification = models.OneToOneField("Notification", on_delete=models.CASCADE, related_name="whatsapp_settings")
    whatsapp_template = models.TextField(null=True, blank=True)


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
    notification_history = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.type}: {self.title}"
