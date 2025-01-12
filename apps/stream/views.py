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
        logger.info("Step 1: Incoming data: %s", request.data)
        try:
            # Step 2: Validate and save
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            stream_image = serializer.save()
            logger.info("Step 2: Validated data, saved StreamImage")

            image_file = request.FILES.get('image')
            if not image_file:
                logger.error("No image provided")
                return Response({"error": "No image provided"}, status=400)

            # Log image info
            logger.info("Incoming image filename: %s", image_file.name)
            logger.info("Incoming image size: %s bytes", image_file.size)

            # For safety, log only a small snippet of bytes
            image_bytes = image_file.read()
            first_64 = image_bytes[:64].hex()
            logger.info("Image content (first 64 bytes in hex): %s", first_64)

            # Reset pointer and continue with YOLO
            image_file.seek(0)

            logger.info("Step 4: YOLO detection started")
            # Save image first
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            stream_image = serializer.save()

            # Process with YOLO
            model = YOLO('yolov8n.pt')
            model.to('cuda')  # Move model to GPU
            # Reset file pointer and read image
            image_file.seek(0)
            image_bytes = image_file.read()

            # Convert to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_array = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img_array is None:
                raise ValueError("Failed to decode image")

            # Run detection with confidence threshold
            results = model(img_array, conf=0.5)[0]

            # Draw bounding boxes if detections are found
            if len(results.boxes) > 0:
                for box in results.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy)
                    cv2.rectangle(img_array, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img_array, f'{box.conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # Save the image with detections
                output_path = 'path/to/save/detected_image.jpg'
                cv2.imwrite(output_path, img_array)

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
            logger.info("Step 5: YOLO detection completed")

            # Final step: Return response
            logger.info("Step 6: Returning response")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error in StreamImageViewSet.create: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

@api_view(['GET'])
def debug_view(request):
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Method: {request.method}")
    logger.info(f"Data: {request.data}")
    return Response({"status": "debug info logged"})
