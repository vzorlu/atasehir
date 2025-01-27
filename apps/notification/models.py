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
    app_key = models.CharField(max_length=255, verbose_name="Uygulama Anahtarı")
    app_secret = models.CharField(max_length=255, verbose_name="Uygulama Gizli Anahtarı")
    device_token = models.TextField(
        verbose_name="Cihaz Token", help_text="Push notification gönderilecek cihaz token'ı"
    )

    class Meta:
        verbose_name = "Push Notification Ayarları"
        verbose_name_plural = "Push Notification Ayarları"


class Notification(models.Model):
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


#
