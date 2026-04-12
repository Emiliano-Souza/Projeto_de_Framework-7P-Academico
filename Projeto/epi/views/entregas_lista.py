from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from epi.models import EntregaEPI, Funcionario


@login_required
def listar_entregas_view(request):
    busca = request.GET.get("busca", "").strip()
    status = request.GET.get("status", "")
    funcionario_id = request.GET.get("funcionario", "")

    qs = EntregaEPI.objects.select_related(
        "funcionario", "epi_lote__epi", "usuario_entrega"
    ).order_by("-data_entrega", "-id")

    if busca:
        qs = qs.filter(funcionario__nome_completo__icontains=busca) | \
             qs.filter(epi_lote__epi__nome__icontains=busca)
        qs = qs.distinct()

    if status:
        qs = qs.filter(status=status)

    if funcionario_id:
        qs = qs.filter(funcionario_id=funcionario_id)

    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    entregas = paginator.get_page(page)

    return render(request, "epi/listar_entregas.html", {
        "titulo_pagina": "Entregas de EPI",
        "entregas": entregas,
        "busca": busca,
        "status": status,
        "funcionario_id": funcionario_id,
        "status_choices": EntregaEPI.Status.choices,
        "funcionarios": Funcionario.objects.filter(ativo=True).order_by("nome_completo"),
    })
