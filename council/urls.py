from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import NotificationsView

urlpatterns = [
    path(
        "detaylar",
        login_required(NotificationsView.as_view(template_name="raporlar.html")),
        name="detaylar",
    ),
    path(
        "mahalleler",
        login_required(NotificationsView.as_view(template_name="mahalleler.html")),
        name="mahalleler",
    ),
]
