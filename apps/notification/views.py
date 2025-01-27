from django.views.generic import TemplateView
from web_project import TemplateLayout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NotificationRuleSerializer
from .models import NOTIFICATION_TYPES, MailSettings, SmsSettings, WhatsappSettings
from .models import Notification


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


@api_view(["POST"])
def send_notification(request):
    class_field = request.data.get("class_field")
    if not class_field:
        return Response({"success": False, "error": "class_field is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Find matching rules for the class
    notifications = Notification.objects.filter(class_field=class_field, enabled=True)

    if not notifications.exists():
        return Response({"success": False, "error": "No matching rules found"}, status=status.HTTP_404_NOT_FOUND)

    results = []
    for notification in notifications:
        channels = notification.channels.all()

        for channel in channels:
            try:
                if channel.name == NOTIFICATION_TYPES.EMAIL:
                    mail_settings = notification.mail_settings
                    # Send email logic
                    results.append({"channel": "email", "status": "sent"})

                elif channel.name == NOTIFICATION_TYPES.SMS:
                    sms_settings = notification.sms_settings
                    # Send SMS logic
                    results.append({"channel": "sms", "status": "sent"})

                elif channel.name == NOTIFICATION_TYPES.WHATSAPP:
                    wa_settings = notification.whatsapp_settings
                    # Send WhatsApp logic
                    results.append({"channel": "whatsapp", "status": "sent"})

            except Exception as e:
                results.append({"channel": channel.name, "status": "failed", "error": str(e)})

    return Response({"success": True, "results": results}, status=status.HTTP_200_OK)
