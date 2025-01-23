import os
import tempfile
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, action
import logging
from .models import StreamImage, Detection
from .serializers import StreamImageSerializer, DetectionSerializer
from ultralytics import YOLO
from django.db.models import Count, Exists, OuterRef

logger = logging.getLogger(__name__)

# Initialize YOLO model at module level
yolo_model = YOLO("yolov8n.pt")


def extract_area(address):
    parts = [part.strip() for part in address.split(",")]
    print(parts)
    for part in parts:
        if "Sokak" in part:
            return part
        elif "Caddesi" in part:
            print(part)
            return part

    # If no street/avenue found, return neighborhood
    for part in parts:
        if part and part not in ["", " "]:
            print(part)
            return part

    return None


class StreamImageViewSet(viewsets.ModelViewSet):
    queryset = StreamImage.objects.all()  # Add base queryset
    serializer_class = StreamImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        base_queryset = StreamImage.objects.all()

        has_detections = self.request.query_params.get("has_detections", None)
        if has_detections == "true":
            # Use exists() subquery instead of annotation
            detections_exist = Detection.objects.filter(image=OuterRef("pk"))
            base_queryset = base_queryset.annotate(has_detections=Exists(detections_exist)).filter(has_detections=True)

        return base_queryset.prefetch_related("detections")

    def create(self, request, *args, **kwargs):
        logger.info("Step 1: Incoming data: %s", request.data)
        temp_file = None

        try:
            # Extract area from fulladdress
            fulladdress = request.data.get("fulladdress", [""])
            print("--fa", fulladdress)
            area = extract_area(fulladdress)

            # Update request data with area
            mutable_data = request.data.copy()
            mutable_data["area"] = area

            # Validate and save StreamImage
            serializer = self.get_serializer(data=mutable_data)
            serializer.is_valid(raise_exception=True)
            stream_image = serializer.save()
            logger.info("Step 2: Validated data, saved StreamImage")

            # Get image file
            image_file = request.FILES.get("image")
            if not image_file:
                raise ValueError("No image provided")

            # Save image content to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            for chunk in image_file.chunks():
                temp_file.write(chunk)
            temp_file.close()

            # Process YOLO detections
            logger.info("Step 4: YOLO detection started")
            results = yolo_model.predict(source=temp_file.name)

            # Create Detection objects
            for r in results[0].boxes.data:
                x1, y1, x2, y2, conf, cls = r.tolist()
                Detection.objects.create(
                    image=stream_image,
                    class_name=results[0].names[int(cls)],
                    x_coord=float(x1),
                    y_coord=float(y1),
                    confidence=float(conf),
                )

            logger.info("Step 5: YOLO detection completed")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error in StreamImageViewSet.create: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Cleanup temporary file
            if temp_file and os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def with_detections(self, request):
        queryset = StreamImage.objects.annotate(detection_count=Count("detections")).filter(detection_count__gt=0)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer


@api_view(["GET"])
def debug_view(request):
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Method: {request.method}")
    logger.info(f"Data: {request.data}")
    return Response({"status": "debug info logged"})
