from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from epi.forms import EntregaEPIForm
from epi.services.entregas import registrar_entrega_epi


@login_required
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
            if hasattr(exc, "message_dict"):
                for field, errors in exc.message_dict.items():
                    for error in errors:
                        if field in form.fields:
                            form.add_error(field, error)
                        else:
                            form.add_error(None, error)
            else:
                form.add_error(None, exc.message)
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
