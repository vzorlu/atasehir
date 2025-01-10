from rest_framework import serializers
from .models import StreamImage, Detection

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = ['id', 'image', 'class_name', 'x_coord', 'y_coord', 'confidence', 'timestamp']

class StreamImageSerializer(serializers.ModelSerializer):
    detections = DetectionSerializer(many=True, read_only=True, source='detection_set')

    class Meta:
        model = StreamImage
        fields = ['id', 'image', 'timestamp', 'processed', 'lang', 'long', 'uuid', 'fulladdress', 'detections']
