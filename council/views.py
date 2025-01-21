from django.views.generic import TemplateView
from stream.models import StreamImage
from web_project import TemplateLayout


class NotificationsView(TemplateView):
    template_name = "raporlar.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["stream_images"] = StreamImage.objects.all().prefetch_related("detection_set")
        return context
