from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from epi.forms import EntregaEPIForm
from epi.services.entregas import registrar_entrega_epi
from epi.views.utils import aplicar_erros_ao_form, grupo_required


@grupo_required("Administrador", "Almoxarife")
def registrar_entrega_view(request):
    form = EntregaEPIForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            registrar_entrega_epi(
                funcionario=form.cleaned_data["funcionario"],
                epi_lote=form.cleaned_data["epi_lote"],
                quantidade_entregue=form.cleaned_data["quantidade_entregue"],
                usuario_entrega=request.user,
                data_entrega=form.cleaned_data["data_entrega"],
                confirmado_recebimento=form.cleaned_data["confirmado_recebimento"],
                observacao=form.cleaned_data["observacao"],
            )
        except ValidationError as exc:
            aplicar_erros_ao_form(exc, form)
        else:
            messages.success(request, "Entrega registrada com sucesso.")
            return redirect("epi:registrar_entrega")

    return render(
        request,
        "epi/registrar_entrega.html",
        {
            "form": form,
            "titulo_pagina": "Registrar Entrega de EPI",
        },
    )

