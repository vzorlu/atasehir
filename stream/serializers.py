from rest_framework import serializers
from .models import StreamImage, Detection


class StreamDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = ["id", "class_name", "x_coord", "y_coord", "confidence", "timestamp"]


class StreamImageSerializer(serializers.ModelSerializer):
    detections = StreamDetectionSerializer(many=True, read_only=True)

    class Meta:
        model = StreamImage
        fields = ["id", "image", "timestamp", "processed", "lang", "long", "fulladdress", "deviceuuid", "detections"]
