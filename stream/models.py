from django.db import models
from apps.notification.models import Notification, NOTIFICATION_TYPES


class StreamImage(models.Model):
    image = models.ImageField(upload_to="stream_images/")
    timestamp = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    lang = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    fulladdress = models.TextField(null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    deviceuuid = models.CharField(max_length=255, null=True, blank=True)  # Renamed from 'device'

    def __str__(self):
        return f"StreamImage {self.id} - {self.timestamp}"


class Detection(models.Model):
    image = models.ForeignKey(StreamImage, related_name="detections", on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    x_min = models.FloatField(default=0.0)
    y_min = models.FloatField(default=0.0)
    x_max = models.FloatField(default=0.0)
    y_max = models.FloatField(default=0.0)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    notification = models.ForeignKey(
        Notification, on_delete=models.SET_NULL, null=True, blank=True, related_name="detections"
    )

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            notification = Notification.objects.create(
                type=NOTIFICATION_TYPES.INFO,
                title=f"New {self.class_name} Detection",
                message=f"Detected {self.class_name} with {self.confidence:.2f} confidence",
            )
            self.notification = notification
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detection {self.id} - {self.class_name}"
