from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
import logging
from .models import StreamImage, Detection
from .serializers import StreamImageSerializer, StreamDetectionSerializer
from ultralytics import YOLO

logger = logging.getLogger(__name__)

# Initialize YOLO model at module level
yolo_model = YOLO("yolov8n.pt")


class StreamImageViewSet(viewsets.ModelViewSet):
    queryset = StreamImage.objects.prefetch_related("detections").all()
    serializer_class = StreamImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        logger.info("Step 1: Incoming data: %s", request.data)
        try:
            # Step 2: Validate and save StreamImage
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            stream_image = serializer.save()
            logger.info("Step 2: Validated data, saved StreamImage")

            image_file = request.FILES.get("image")
            if not image_file:
                logger.error("No image provided")
                return Response({"error": "No image provided"}, status=400)

            # Log image info
            logger.info(f"Incoming image filename: {image_file.name}")
            logger.info(f"Incoming image size: {image_file.size} bytes")

            # Process YOLO detections
            logger.info("Step 4: YOLO detection started")
            results = yolo_model.predict(source=image_file, imgsz=640)

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

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = StreamDetectionSerializer


@api_view(["GET"])
def debug_view(request):
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Method: {request.method}")
    logger.info(f"Data: {request.data}")
    return Response({"status": "debug info logged"})
