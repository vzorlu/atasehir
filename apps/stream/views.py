from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
import logging
from .models import StreamImage, Detection
from .serializers import StreamImageSerializer, DetectionSerializer
from ultralytics import YOLO
import cv2
import numpy as np

logger = logging.getLogger(__name__)

class StreamImageViewSet(viewsets.ModelViewSet):
    queryset = StreamImage.objects.all()
    serializer_class = StreamImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        try:
            # Get and validate image
            image_file = request.FILES.get('image')
            if not image_file:
                return Response(
                    {'error': 'No image provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save image first
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            stream_image = serializer.save()

            # Process with YOLO
            model = YOLO('yolov8n.pt')
            model.conf = 0.5
            model.device = 'gpu'
            # Reset file pointer and read image
            image_file.seek(0)
            image_bytes = image_file.read()

            # Convert to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_array = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img_array is None:
                raise ValueError("Failed to decode image")

            # Run detection
            results = model(img_array)[0]

            # Save detections
            for result in results.boxes.data:
                Detection.objects.create(
                    image=stream_image,
                    class_name=model.names[int(result[5])],
                    x_coord=float(result[0]),
                    y_coord=float(result[1]),
                    confidence=float(result[4])
                )

            stream_image.processed = True
            stream_image.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

@api_view(['GET'])
def debug_view(request):
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Method: {request.method}")
    logger.info(f"Data: {request.data}")
    return Response({"status": "debug info logged"})
