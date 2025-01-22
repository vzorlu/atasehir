from django.views.generic import TemplateView
from stream.models import StreamImage
from web_project import TemplateLayout
from django.conf import settings


class CouncilView(TemplateView):
    template_name = "harita-raporlari.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["stream_images"] = StreamImage.objects.prefetch_related("detections").all()
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        print("google_maps_api_key", context["google_maps_api_key"])
        return context
