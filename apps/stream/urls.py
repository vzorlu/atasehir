from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StreamImageViewSet, DetectionViewSet, debug_view

router = DefaultRouter()
router.register(r'images', StreamImageViewSet)
router.register(r'detections', DetectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('debug/', debug_view, name='debug'),
]
