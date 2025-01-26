from django.views.generic import TemplateView
from web_project import TemplateLayout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NotificationRuleSerializer
from .models import MailSettings, SmsSettings, WhatsappSettings


class NotificationsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


@api_view(["POST"])
def create_notification_rule(request):
    serializer = NotificationRuleSerializer(data=request.data)
    if serializer.is_valid():
        notification = serializer.save()

        # Create settings if channels are selected
        if "channels" in request.data:
            channels = request.data.getlist("channels[]")
            if "email" in channels:
                MailSettings.objects.create(notification=notification)
            if "sms" in channels:
                SmsSettings.objects.create(notification=notification)
            if "whatsapp" in channels:
                WhatsappSettings.objects.create(notification=notification)

        return Response({"success": True}, status=status.HTTP_201_CREATED)
    return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
