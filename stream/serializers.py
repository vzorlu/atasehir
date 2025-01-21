from rest_framework import serializers
from .models import StreamImage, Detection

class StreamImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamImage
        fields = '__all__'

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'
