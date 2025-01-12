from rest_framework import serializers
from .models import StreamImage, Detection

class StreamImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamImage
        fields = '__all__'
        extra_kwargs = {
            'image_processing': {'required': False}  # Make optional
        }

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = ['id', 'image', 'class_name', 'x_coord', 'y_coord', 'confidence', 'timestamp']
