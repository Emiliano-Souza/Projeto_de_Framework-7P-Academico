from django.urls import path

from epi.views.funcionarios import historico_funcionario_view, listar_funcionarios_view

urlpatterns = [
    path("funcionarios/", listar_funcionarios_view, name="listar_funcionarios"),
    path("funcionarios/<int:pk>/", historico_funcionario_view, name="historico_funcionario"),
]
