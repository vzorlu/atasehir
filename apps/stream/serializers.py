from rest_framework import serializers
from .models import StreamImage, Detection

class StreamImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamImage
        fields = [
            'id',
            'image',
            'timestamp',
            'processed',
            'lang',
            'long',
            'fulladdress',
            'deviceuuid'
        ]
        read_only_fields = ['timestamp', 'processed']

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'
