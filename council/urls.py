from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import CouncilView

urlpatterns = [
    path(
        "detaylar",
        login_required(CouncilView.as_view(template_name="raporlar.html")),
        name="detaylar",
    ),
    path(
        "mahalleler",
        login_required(CouncilView.as_view(template_name="mahalleler.html")),
        name="mahalleler",
    ),
]
