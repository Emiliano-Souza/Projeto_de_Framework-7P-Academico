from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from epi.forms import BaixaEPIForm
from epi.services.entregas import registrar_baixa_epi


@login_required
def registrar_baixa_view(request):
    form = BaixaEPIForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            registrar_baixa_epi(
                entrega_id=form.cleaned_data["entrega"].pk,
                quantidade_baixada=form.cleaned_data["quantidade_baixada"],
                usuario_baixa=request.user,
                motivo_baixa=form.cleaned_data["motivo_baixa"],
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
            messages.success(request, "Baixa registrada com sucesso.")
            return redirect("epi:registrar_baixa")

    return render(
        request,
        "epi/registrar_baixa.html",
        {
            "form": form,
            "titulo_pagina": "Registrar Baixa de EPI",
        },
    )
