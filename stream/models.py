from django.db import models


class StreamImage(models.Model):
    image = models.ImageField(upload_to="stream_images/")
    timestamp = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    lang = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    fulladdress = models.TextField(null=True, blank=True)
    deviceuuid = models.CharField(max_length=255, null=True, blank=True)  # Renamed from 'device'

    def __str__(self):
        return f"StreamImage {self.id} - {self.timestamp}"


class Detection(models.Model):
    image = models.ForeignKey(StreamImage, related_name="detections", on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    x_coord = models.FloatField()
    y_coord = models.FloatField()
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Detection {self.id} - {self.class_name}"
