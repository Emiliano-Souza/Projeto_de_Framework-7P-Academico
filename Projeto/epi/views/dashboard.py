from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render

from epi.models import EPI, EPILote, EntregaEPI, Funcionario, MovimentacaoEstoque


@login_required
def dashboard_view(request):
    hoje = date.today()
    proximos_dias = hoje + timedelta(days=30)

    lotes_vencidos = EPILote.objects.filter(
        data_validade__lt=hoje,
        quantidade_disponivel__gt=0,
    ).count()

    lotes_proximos = EPILote.objects.filter(
        data_validade__gte=hoje,
        data_validade__lte=proximos_dias,
        quantidade_disponivel__gt=0,
    ).count()

    lotes_estoque_baixo = EPILote.objects.filter(
        quantidade_disponivel__gt=0,
        quantidade_disponivel__lte=F("epi__estoque_minimo"),
    ).exclude(epi__estoque_minimo=0).count()

    alertas = []
    if lotes_vencidos:
        alertas.append({
            "tipo": "erro",
            "icone": "⛔",
            "mensagem": f"{lotes_vencidos} lote(s) vencido(s) ainda com saldo em estoque. Realize a baixa ou descarte.",
        })
    if lotes_proximos:
        alertas.append({
            "tipo": "aviso",
            "icone": "⚠",
            "mensagem": f"{lotes_proximos} lote(s) vencem nos proximos 30 dias. Verifique o estoque.",
        })
    if lotes_estoque_baixo:
        alertas.append({
            "tipo": "aviso",
            "icone": "⚠",
            "mensagem": f"{lotes_estoque_baixo} lote(s) com estoque abaixo do minimo configurado.",
        })

    context = {
        "titulo_pagina": "Dashboard",
        "total_funcionarios_ativos": Funcionario.objects.filter(ativo=True).count(),
        "total_epis": EPI.objects.filter(ativo=True).count(),
        "total_lotes_ativos": EPILote.objects.filter(quantidade_disponivel__gt=0).count(),
        "lotes_vencidos": lotes_vencidos,
        "lotes_proximos_vencimento": lotes_proximos,
        "lotes_estoque_baixo": lotes_estoque_baixo,
        "entregas_pendentes": EntregaEPI.objects.filter(status=EntregaEPI.Status.ENTREGUE).count(),
        "ultimas_movimentacoes": MovimentacaoEstoque.objects.select_related(
            "epi_lote__epi", "usuario", "funcionario"
        ).order_by("-created_at")[:8],
        "alertas": alertas,
    }

    return render(request, "epi/dashboard.html", context)
