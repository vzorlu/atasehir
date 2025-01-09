from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StreamImageViewSet, DetectionViewSet

router = DefaultRouter()
router.register(r'images', StreamImageViewSet)
router.register(r'detections', DetectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
