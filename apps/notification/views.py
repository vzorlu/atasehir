from django.views.generic import TemplateView
from web_project import TemplateLayout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NotificationRuleSerializer
from .models import NOTIFICATION_TYPES
from .models import Notification
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client


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
        serializer.save()

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
                    try:
                        send_mail(
                            subject=notification.title,
                            message=notification.message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[notification.recipient],
                            fail_silently=False,
                        )
                        results.append({"channel": "email", "status": "sent"})
                    except Exception as e:
                        results.append({"channel": "email", "status": "failed", "error": str(e)})
                elif channel.name == NOTIFICATION_TYPES.SMS:
                    try:
                        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        message = client.messages.create(
                            body=notification.message, from_=settings.TWILIO_PHONE_NUMBER, to=notification.recipient
                        )
                        results.append({"channel": "sms", "status": "sent", "message_sid": message.sid})
                    except Exception as e:
                        results.append({"channel": "sms", "status": "failed", "error": str(e)})

                elif channel.name == NOTIFICATION_TYPES.WHATSAPP:
                    try:
                        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        message = client.messages.create(
                            from_=f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}",
                            body=notification.message,
                            to=f"whatsapp:{notification.recipient}",
                        )
                        results.append({"channel": "whatsapp", "status": "sent", "message_sid": message.sid})
                    except Exception as e:
                        results.append({"channel": "whatsapp", "status": "failed", "error": str(e)})

            except Exception as e:
                results.append({"channel": channel.name, "status": "failed", "error": str(e)})

    return Response({"success": True, "results": results}, status=status.HTTP_200_OK)
