from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import NotificationsView

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
            "report",
            login_required(NotificationsView.as_view(template_name="report.html")),
            name="report",
        ),

        path(
            "settings",
            login_required(NotificationsView.as_view(template_name="settings.html")),
            name="settings",
        ),
]
