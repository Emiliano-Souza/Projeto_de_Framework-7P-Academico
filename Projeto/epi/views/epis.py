from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from epi.models import EPI, EPILote
from datetime import date


@login_required
def listar_epis_view(request):
    busca = request.GET.get("busca", "").strip()
    ativo = request.GET.get("ativo", "")

    qs = EPI.objects.order_by("nome")

    if busca:
        qs = qs.filter(nome__icontains=busca) | qs.filter(codigo_interno__icontains=busca)
        qs = qs.distinct()

    if ativo == "1":
        qs = qs.filter(ativo=True)
    elif ativo == "0":
        qs = qs.filter(ativo=False)

    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    epis = paginator.get_page(page)

    return render(request, "epi/listar_epis.html", {
        "titulo_pagina": "EPIs",
        "epis": epis,
        "busca": busca,
        "ativo": ativo,
    })


@login_required
def listar_lotes_view(request):
    busca = request.GET.get("busca", "").strip()
    situacao = request.GET.get("situacao", "")
    hoje = date.today()

    qs = EPILote.objects.select_related("epi").order_by("data_validade", "numero_lote")

    if busca:
        qs = qs.filter(numero_lote__icontains=busca) | qs.filter(epi__nome__icontains=busca)
        qs = qs.distinct()

    if situacao == "vencido":
        qs = qs.filter(data_validade__lt=hoje)
    elif situacao == "disponivel":
        qs = qs.filter(quantidade_disponivel__gt=0)
    elif situacao == "zerado":
        qs = qs.filter(quantidade_disponivel=0)

    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    lotes = paginator.get_page(page)

    return render(request, "epi/listar_lotes.html", {
        "titulo_pagina": "Lotes de EPI",
        "lotes": lotes,
        "busca": busca,
        "situacao": situacao,
        "hoje": hoje,
    })
