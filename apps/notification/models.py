from django.db import models
from django.contrib.auth import get_user_model
from council.models import Department
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

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


class MailSettings(NotificationSettings):
    notification = models.OneToOneField("Notification", on_delete=models.CASCADE, related_name="mail_settings")
    smtp_host = models.CharField(max_length=255, verbose_name="SMTP Sunucu", default="smtp.gmail.com")
    smtp_port = models.IntegerField(verbose_name="SMTP Port", default=587)
    smtp_user = models.CharField(max_length=255, verbose_name="SMTP Kullanıcı", default="user@algi.ai")
    smtp_password = models.CharField(max_length=255, verbose_name="SMTP Şifre", default="default_password")
    from_email = models.EmailField(verbose_name="Gönderen E-posta", default="notifications@algi.ai")
    email_template = models.TextField(null=True, blank=True, verbose_name="E-posta Şablonu")


class SmsSettings(NotificationSettings):
    notification = models.OneToOneField("Notification", on_delete=models.CASCADE, related_name="sms_settings")
    api_key = models.CharField(max_length=255, verbose_name="API Anahtarı", default="default_api_key")
    api_secret = models.CharField(max_length=255, verbose_name="API Gizli Anahtarı", default="default_api_secret")
    sender_name = models.CharField(max_length=11, verbose_name="Gönderen Adı", default="ALGI")
    api_endpoint = models.URLField(verbose_name="API Endpoint", default="https://api.example.com")
    sms_template = models.TextField(null=True, blank=True, verbose_name="SMS Şablonu")


class WhatsappSettings(NotificationSettings):
    notification = models.OneToOneField("Notification", on_delete=models.CASCADE, related_name="whatsapp_settings")
    wa_api_key = models.CharField(max_length=255, verbose_name="WhatsApp API Anahtarı", default="default_wa_api_key")
    wa_api_secret = models.CharField(
        max_length=255, verbose_name="WhatsApp API Gizli Anahtarı", default="default_wa_secret"
    )
    wa_phone_number = models.CharField(max_length=15, verbose_name="WhatsApp Telefon No", default="+905555555555")
    wa_api_endpoint = models.URLField(verbose_name="WhatsApp API Endpoint", default="https://api.whatsapp.com")
    whatsapp_template = models.TextField(null=True, blank=True, verbose_name="WhatsApp Şablonu")


class PushNotification(NotificationSettings):
    notification = models.OneToOneField("Notification", on_delete=models.CASCADE, related_name="push_settings")
    app_key = models.CharField(max_length=255, verbose_name="Uygulama Anahtarı")
    app_secret = models.CharField(max_length=255, verbose_name="Uygulama Gizli Anahtarı")
    device_token = models.TextField(verbose_name="Cihaz Token")


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


@receiver(m2m_changed, sender=Notification.channels.through)
def create_channel_settings(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for channel_id in pk_set:
            channel = NotificationChannel.objects.get(id=channel_id)

            if channel.name == "MAIL":
                MailSettings.objects.get_or_create(notification=instance)
            elif channel.name == "SMS":
                SmsSettings.objects.get_or_create(notification=instance)
            elif channel.name == "WHATSAPP":
                WhatsappSettings.objects.get_or_create(notification=instance)
            elif channel.name == "PUSH":
                PushNotification.objects.get_or_create(notification=instance)
