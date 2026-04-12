from django.urls import path

from epi.views.dashboard import dashboard_view

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
]
