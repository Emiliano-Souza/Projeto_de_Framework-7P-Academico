from django.urls import path

from epi.views.devolucoes import registrar_devolucao_view


urlpatterns = [
    path("devolucoes/nova/", registrar_devolucao_view, name="registrar_devolucao"),
]
