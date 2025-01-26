from rest_framework import serializers
from .models import StreamImage, Detection


class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = ["id", "image", "class_name", "x_min", "y_min", "x_max", "y_max", "confidence", "timestamp"]


class StreamImageSerializer(serializers.ModelSerializer):
    detections = DetectionSerializer(many=True, read_only=True)
    detection_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = StreamImage
        fields = [
            "id",
            "image",
            "timestamp",
            "processed",
            "lang",
            "long",
            "fulladdress",
            "area",
            "deviceuuid",
            "detections",
            "detection_count",
        ]
