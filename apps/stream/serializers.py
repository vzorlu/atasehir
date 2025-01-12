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
    lang = serializers.FloatField(source='image.lang', read_only=True)
    long = serializers.FloatField(source='image.long', read_only=True)

    class Meta:
        model = Detection
        fields = [
            'id',
            'image',
            'class_name',
            'x_coord    ',
            'y_coord',
            'confidence',
            'timestamp',
            'lang',
            'long'
        ]
