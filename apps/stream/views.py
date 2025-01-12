from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import StreamImage, Detection
from .serializers import StreamImageSerializer, DetectionSerializer
from ultralytics import YOLO
import cv2
import numpy as np
import torch
from .models import save_processed_image  # Import the save function
import logging

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
            model.device = 'cuda' if torch.cuda.is_available() else 'cpu'
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

            # Draw detections on the image
            for result in results.boxes.data:
                Detection.objects.create(
                    image=stream_image,
                    class_name=model.names[int(result[5])],
                    x_coord=float(result[0]),
                    y_coord=float(result[1]),
                    confidence=float(result[4])
                )
                # Draw bounding box
                cv2.rectangle(img_array, (int(result[0]), int(result[1])), (int(result[2]), int(result[3])), (0, 255, 0), 2)

            # Save the processed image
            processed_image_path = save_processed_image(img_array)
            if processed_image_path:
                stream_image.image_processing = processed_image_path
                stream_image.processed = True
                stream_image.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error in StreamImageViewSet.create: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer
