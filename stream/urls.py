from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets  # Add this import
from .views import StreamImageViewSet, DetectionViewSet, debug_view
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

router = DefaultRouter()
router.register(r'images', StreamImageViewSet)
router.register(r'detections', DetectionViewSet)

class StreamImageViewSet(viewsets.ModelViewSet):
    # ...existing code...

    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, *args, **kwargs):
        print(f"StreamImageViewSet: {self.request.method} request received")
        response = super().dispatch(*args, **kwargs)
        print(f"StreamImageViewSet: {self.request.method} response: {response.status_code}")
        return response

class DetectionViewSet(viewsets.ModelViewSet):
    # ...existing code...

    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, *args, **kwargs):
        print(f"DetectionViewSet: {self.request.method} request received")
        response = super().dispatch(*args, **kwargs)
        print(f"DetectionViewSet: {self.request.method} response: {response.status_code}")
        return response

urlpatterns = [
    path('', include(router.urls)),
    path('debug/', debug_view, name='debug'),
]
