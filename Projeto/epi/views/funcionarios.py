from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from epi.models import EntregaEPI, Funcionario, Setor


@login_required
def listar_funcionarios_view(request):
    busca = request.GET.get("busca", "").strip()
    setor_id = request.GET.get("setor", "")
    ativo = request.GET.get("ativo", "")

    qs = Funcionario.objects.select_related("setor").order_by("nome_completo")

    if busca:
        qs = qs.filter(nome_completo__icontains=busca) | qs.filter(matricula__icontains=busca)
        qs = qs.distinct()

    if setor_id:
        qs = qs.filter(setor_id=setor_id)

    if ativo == "1":
        qs = qs.filter(ativo=True)
    elif ativo == "0":
        qs = qs.filter(ativo=False)

    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    funcionarios = paginator.get_page(page)

    return render(request, "epi/listar_funcionarios.html", {
        "titulo_pagina": "Funcionarios",
        "funcionarios": funcionarios,
        "setores": Setor.objects.filter(ativo=True).order_by("nome"),
        "busca": busca,
        "setor_id": setor_id,
        "ativo": ativo,
    })


@login_required
def historico_funcionario_view(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)

    entregas = list(
        EntregaEPI.objects.filter(funcionario=funcionario)
        .select_related("epi_lote__epi", "usuario_entrega")
        .order_by("-data_entrega")
    )

    for e in entregas:
        e.saldo_aberto = e.quantidade_entregue - e.quantidade_devolvida - e.quantidade_baixada

    saldo_aberto_total = sum(e.saldo_aberto for e in entregas)

    return render(request, "epi/historico_funcionario.html", {
        "titulo_pagina": f"Historico — {funcionario.nome_completo}",
        "funcionario": funcionario,
        "entregas": entregas,
        "saldo_aberto": saldo_aberto_total,
    })
