from django.db import models

class StreamImage(models.Model):
    image = models.ImageField(upload_to='stream_images/')
    image_processing = models.ImageField(upload_to='stream_images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=True)
    lang = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    fulladdress = models.TextField(null=True, blank=True)
    deviceuuid = models.CharField(max_length=255)

    def __str__(self):
        return f"StreamImage {self.id} - {self.timestamp}"

class Detection(models.Model):
    image = models.ForeignKey(StreamImage, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    x_coord = models.FloatField()
    y_coord = models.FloatField()
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Detection {self.id} - {self.class_name}"
