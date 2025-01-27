from django.db import models
from django.contrib.auth import get_user_model
from council.models import Department

User = get_user_model()


class NOTIFICATION_TYPES:
    REPORT_ONLY = "REPORT_ONLY"
    DEPARTMENT_NOTIFY = "DEPARTMENT_NOTIFY"
    PERSON_NOTIFY = "PERSON_NOTIFY"
    SMS = "SMS"
    EMAIL = "EMAIL"
    WHATSAPP = "WHATSAPP"

    CHOICES = [
        (REPORT_ONLY, "Sadece Raporla"),
        (DEPARTMENT_NOTIFY, "Departmana Bildir"),
        (PERSON_NOTIFY, "Kişiye Bildir"),
        (SMS, "SMS Gönder"),
        (EMAIL, "E-posta Gönder"),
        (WHATSAPP, "WhatsApp Gönder"),
    ]


class SEVERITY_LEVELS:
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    CHOICES = [
        (LOW, "Düşük"),
        (MEDIUM, "Orta"),
        (HIGH, "Yüksek"),
        (CRITICAL, "Kritik"),
    ]


class NotificationSettings(models.Model):
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NotificationChannel(models.Model):
    name = models.CharField(max_length=20, choices=NOTIFICATION_TYPES.CHOICES)

    class Meta:
        verbose_name = "Bildirim Kanalı"
        verbose_name_plural = "Bildirim Kanalları"

    def __str__(self):
        return self.get_name_display()


class Notification(models.Model):
    rule_name = models.CharField(
        max_length=255,
        default="Varsayılan Kural",
        verbose_name="Kural Adı",
    )
    channels = models.ManyToManyField(
        NotificationChannel, verbose_name="Bildirim Kanalları", help_text="Birden fazla kanal seçebilirsiniz"
    )
    title = models.CharField(
        max_length=255,
        default="Varsayılan Kural",  # Add default value
        verbose_name="Kural Adı",
        help_text="Bu kuralın tanımlayıcı adı",
    )
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES.CHOICES, default=NOTIFICATION_TYPES.REPORT_ONLY)
    message = models.TextField()
    class_field = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications"
    )
    notification_history = models.JSONField(default=list, blank=True)
    severity = models.CharField(
        max_length=10, choices=SEVERITY_LEVELS.CHOICES, default=SEVERITY_LEVELS.MEDIUM, verbose_name="Uyarı Düzeyi"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.type}: {self.rule_name}"  # Update str method to use rule_name
