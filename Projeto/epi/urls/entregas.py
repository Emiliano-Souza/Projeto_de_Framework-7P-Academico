from django.urls import path

from epi.views.entregas import registrar_entrega_view


urlpatterns = [
    path("entregas/nova/", registrar_entrega_view, name="registrar_entrega"),
]

