from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from epi.models import MovimentacaoEstoque


@login_required
def listar_movimentacoes_view(request):
    movimentacoes = (
        MovimentacaoEstoque.objects.select_related(
            "epi_lote",
            "epi_lote__epi",
            "funcionario",
            "usuario",
        )
        .order_by("-created_at", "-id")
    )

    return render(
        request,
        "epi/listar_movimentacoes.html",
        {
            "titulo_pagina": "Historico de Movimentacoes de Estoque",
            "movimentacoes": movimentacoes,
        },
    )
