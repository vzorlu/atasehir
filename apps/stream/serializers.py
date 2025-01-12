from rest_framework import serializers
from .models import StreamImage, Detection

class StreamImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamImage
        fields = '__all__'

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = ['id', 'image', 'class_name', 'x_coord', 'y_coord', 'confidence', 'timestamp']
