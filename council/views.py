from django.views.generic import TemplateView
from stream.models import StreamImage
from web_project import TemplateLayout
from django.conf import settings
from django.shortcuts import render


class CouncilView(TemplateView):
    template_name = "harita-raporlari.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Get images with detections, including all required fields
        images_with_detections = StreamImage.objects.filter().prefetch_related("detections").order_by("-timestamp")

        context["stream_images"] = images_with_detections
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        return context


def images_with_detections(request):
    stream_images = StreamImage.objects.all().order_by("-timestamp")

    context = {"stream_images": stream_images, "layout_path": "layouts/content.html"}

    return render(request, "raporlar.html", context)
