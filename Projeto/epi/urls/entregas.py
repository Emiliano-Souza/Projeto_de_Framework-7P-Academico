from django.urls import path

from epi.views.entregas import registrar_entrega_view
from epi.views.entregas_lista import listar_entregas_view

urlpatterns = [
    path("entregas/nova/", registrar_entrega_view, name="registrar_entrega"),
    path("entregas/", listar_entregas_view, name="listar_entregas"),
]
