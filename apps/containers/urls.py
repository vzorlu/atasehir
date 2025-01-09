from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ContainersView

urlpatterns = [

path(
        "container",
        login_required(ContainersView.as_view(template_name="index.html")),
        name="container",
    ),

]
