from django.urls import path, include
from .views import (
    DashboardsView
)
from django.contrib.auth.decorators import login_required

urlpatterns = [

    # Dashboard Sayfaları
    path(
        "",
        login_required(DashboardsView.as_view(template_name="dashboard_analytics.html")),
        name="index",
    ),
    path(
        "dashboard/crm/",
        login_required(DashboardsView.as_view(template_name="dashboard_crm.html")),
        name="dashboard-crm",
    ),
    path(
        "dashboard/ready-models/",
        login_required(DashboardsView.as_view(template_name="dashboard_models.html")),
        name="dashboard-models",
    ),
    path(
        "dashboard/task/",
        login_required(DashboardsView.as_view(template_name="dashboard_task.html")),
        name="dashboard-task",
    )
]
