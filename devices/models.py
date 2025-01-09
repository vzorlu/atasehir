from django.db import models
from django.utils import timezone
from django.conf import settings
from onesignal_sdk.client import Client
from django.db.models.signals import post_save
from django.dispatch import receiver


class Device(models.Model):
    device_id = models.AutoField(primary_key=True)  # Otomatik artan ID
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    license_key = models.ForeignKey('License', on_delete=models.SET_NULL, null=True, blank=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    mac_address = models.CharField(max_length=100, unique=True, blank=True, null=True)
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True, blank=True)
    ssh_username = models.CharField(max_length=100, blank=True, null=True)
    ssh_password = models.CharField(max_length=100, blank=True, null=True)
    tunnel_info = models.JSONField(blank=True, null=True)
    cpu_info = models.CharField(max_length=255, blank=True, null=True)
    gpu_info = models.CharField(max_length=255, blank=True, null=True)

    DEVICE_TYPE_CHOICES = [
        ('NVIDIA_GPU', 'NVIDIA GPU'),
        ('INTEL_CPU', 'Intel CPU'),
        ('CPU', 'CPU'),
        ('JETSON', 'Jetson'),
    ]
    type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES, blank=True, null=True)

    INFRASTRUCTURE_CHOICES = [
        ('ON_PREMISE', 'On-Premise'),
        ('CLOUD', 'Cloud'),
    ]
    infrastructure = models.CharField(max_length=50, choices=INFRASTRUCTURE_CHOICES, blank=True, null=True)

    OPERATING_SYSTEM_CHOICES = [
        ('UBUNTU', 'Ubuntu'),
        ('WINDOWS', 'Windows'),
    ]
    operating_system = models.CharField(max_length=50, choices=OPERATING_SYSTEM_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else f"Device {self.device_id}"


class License(models.Model):
    LICENSE_TYPE_CHOICES = [
        ('DEMO', 'Demo'),
        ('TIMED', 'Süreli'),
        ('UNLIMITED', 'Süresiz'),
    ]
    license_key = models.CharField(max_length=100, unique=True)
    license_type = models.CharField(max_length=50, choices=LICENSE_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    available_devices = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.license_key} ({self.license_type})"


class DeviceData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_space = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.device.device_id} - {self.timestamp}"


class DeviceReport(models.Model):
    mac_address = models.CharField(max_length=100)
    data = models.JSONField()  # Cihaz verilerini JSON formatında tutar
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.mac_address} at {self.created_at}"


class Notification(models.Model):
    title = models.CharField(max_length=200, verbose_name="Bildirim Başlığı")
    message = models.TextField(verbose_name="Bildirim Mesajı")
    image = models.URLField(max_length=500, blank=True, null=True, verbose_name="Görsel URL")  # Yeni: Görsel URL
    camera = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kamera Bilgisi")  # Yeni: Kamera bilgisi
    alertLevel = models.CharField(max_length=50, blank=True, null=True, verbose_name="Uyarı Seviyesi")  # Yeni: Uyarı seviyesi
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kategori")  # Yeni: Kategori bilgisi
    segment = models.CharField(max_length=100, default='All', verbose_name="Hedef Segment")  # 'All', 'Subscribed Users', vb.
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderim Zamanı")
    status = models.CharField(max_length=50, default="Pending", verbose_name="Durum")  # Bildirim durumu

    def __str__(self):
        return self.title

    def send_push_notification(self):
        client = Client(app_id=settings.ONESIGNAL_APP_ID, rest_api_key=settings.ONESIGNAL_API_KEY)

        # Bildirim içeriğini tanımlar
        notification_body = {
            'contents': {'en': self.message},
            'headings': {'en': self.title},
            'included_segments': [self.segment],
            'data': {
                'image': self.image,
                'camera': self.camera,
                'alertLevel': self.alertLevel,
                'category': self.category
            },
        }

        # Opsiyonel olarak büyük resim eklemek (yalnızca varsa)
        if self.image:
            notification_body['big_picture'] = self.image

        # Bildirimi gönder ve yanıtı kontrol et
        response = client.send_notification(notification_body)
        if response.status_code == 200:
            self.status = "Sent"
        else:
            self.status = "Failed"

        # Status alanını günceller
        self.save(update_fields=["status"])
        return response


    # Notification kaydedildikten sonra push notification gönderir
@receiver(post_save, sender=Notification)
def send_notification_on_save(sender, instance, created, **kwargs):
    if created:  # Yeni bir kayıt oluşturulmuşsa bildirimi gönder
        instance.send_push_notification()
