from django.urls import path

from epi.views.baixas import registrar_baixa_view


urlpatterns = [
    path("baixas/nova/", registrar_baixa_view, name="registrar_baixa"),
]
