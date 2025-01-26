from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import NotificationsView, create_notification_rule

urlpatterns = [
    path(
        "notification",
        login_required(NotificationsView.as_view(template_name="notification.html")),
        name="notification",
    ),
    path(
        "notification-channels",
        login_required(NotificationsView.as_view(template_name="notification-channels.html")),
        name="notification-channels",
    ),
    path(
        "settings",
        login_required(NotificationsView.as_view(template_name="settings.html")),
        name="settings",
    ),
    path("api/notifications/rule/", create_notification_rule, name="create_notification_rule"),
]
