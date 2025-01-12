from django.db import models
from datetime import datetime
import os
import cv2
from pathlib import Path

class StreamImage(models.Model):
    image = models.ImageField(upload_to='stream_images/')
    image_processing = models.ImageField(upload_to='processed_images/', null=True, blank=True)
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

def save_processed_image(image, base_path='processed_images'):
    # Create directory if not exists
    Path(base_path).mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'yolo_processed_{timestamp}.jpg'

    # Full path for saving
    save_path = os.path.join(base_path, filename)

    try:
        # Save the processed image
        cv2.imwrite(save_path, image)
        return save_path
    except Exception as e:
        print(f"Error saving processed image: {e}")
        return None

# Update existing image_processing function
def image_processing(frame):
    try:
        # ...existing YOLO processing code...

        # After YOLO drawing is complete, save the processed image
        save_processed_image(frame)

        return frame
    except Exception as e:
        print(f"Error in image processing: {e}")
        return frame
