from django.urls import path

from epi.views.movimentacoes import listar_movimentacoes_view


urlpatterns = [
    path("movimentacoes/", listar_movimentacoes_view, name="listar_movimentacoes"),
]
