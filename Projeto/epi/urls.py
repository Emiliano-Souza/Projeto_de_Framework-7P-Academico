from django.urls import path

from epi.views import registrar_entrega_view


app_name = "epi"


urlpatterns = [
    path("entregas/nova/", registrar_entrega_view, name="registrar_entrega"),
]
