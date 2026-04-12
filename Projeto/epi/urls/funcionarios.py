from django.urls import path

from epi.views.funcionarios import listar_funcionarios_view

urlpatterns = [
    path("funcionarios/", listar_funcionarios_view, name="listar_funcionarios"),
]
