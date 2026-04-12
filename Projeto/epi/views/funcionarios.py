from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from epi.models import Funcionario, Setor


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
