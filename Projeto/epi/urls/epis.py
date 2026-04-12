from django.urls import path

from epi.views.epis import listar_epis_view, listar_lotes_view

urlpatterns = [
    path("epis/", listar_epis_view, name="listar_epis"),
    path("lotes/", listar_lotes_view, name="listar_lotes"),
]
