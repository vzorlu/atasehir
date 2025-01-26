from django.views.generic import TemplateView
from stream.models import StreamImage
from web_project import TemplateLayout
from django.conf import settings
from django.shortcuts import render
from django.template.defaulttags import register
from apps.notification.models import Notification


@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    try:
        return dictionary.get(key)
    except AttributeError:
        return None


class CouncilView(TemplateView):
    template_name = "harita-raporlari.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Get images with detections, including all required fields
        images_with_detections = StreamImage.objects.all().order_by("-timestamp")
        context["stream_images"] = images_with_detections
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY

        notification_rules = {
            notification.class_field: {
                "type": notification.type,
                "title": notification.title,
                "message": notification.message,
                "department": notification.department_id,
            }
            for notification in Notification.objects.all()
        }
        context["notification_rules"] = notification_rules

        return context


def images_with_detections(request):
    stream_images = StreamImage.objects.prefetch_related("detections").order_by("-id")  # Using correct related_name

    context = {"stream_images": stream_images, "layout_path": "layouts/content.html"}
    return render(request, "raporlar.html", context)
