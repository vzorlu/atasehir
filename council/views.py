from django.views.generic import TemplateView
from stream.models import StreamImage
from web_project import TemplateLayout
from django.conf import settings


class CouncilView(TemplateView):
    template_name = "harita-raporlari.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Get images with detections, including all required fields
        images_with_detections = StreamImage.objects.filter().prefetch_related("detections").order_by("timestamp")

        context["stream_images"] = images_with_detections
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        return context


"""
from django.views.generic import TemplateView
from django.db.models import Count
from stream.models import StreamImage
from web_project import TemplateLayout
from django.conf import settings


class CouncilView(TemplateView):
    template_name = "harita-raporlari.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Get images with detections, including all required fields
        images_with_detections = (
            StreamImage.objects.filter(
                id__in=StreamImage.objects.values("id")
                .annotate(detection_count=Count("detections"))
                .filter(detection_count__gt=0)
                .values_list("id", flat=True)
            )
            .prefetch_related("detections")
            .order_by("-timestamp")
        )

        context["stream_images"] = images_with_detections
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        return context

"""
