from django.views.generic import TemplateView
from django.db.models import Count
from stream.models import StreamImage
from web_project import TemplateLayout
from django.conf import settings


class CouncilView(TemplateView):
    template_name = "harita-raporlari.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["stream_images"] = (
            StreamImage.objects.annotate(detection_count=Count("detections"))
            .filter(detection_count__gt=0)
            .prefetch_related("detections")
            .all()
        )
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        return context
