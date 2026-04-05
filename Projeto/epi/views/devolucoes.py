from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from epi.forms import DevolucaoEPIForm
from epi.services.entregas import registrar_devolucao_epi


@login_required
def registrar_devolucao_view(request):
    form = DevolucaoEPIForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            registrar_devolucao_epi(
                entrega_id=form.cleaned_data["entrega"].pk,
                quantidade_devolvida=form.cleaned_data["quantidade_devolvida"],
                usuario_devolucao=request.user,
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
            messages.success(request, "Devolucao registrada com sucesso.")
            return redirect("epi:registrar_devolucao")

    return render(
        request,
        "epi/registrar_devolucao.html",
        {
            "form": form,
            "titulo_pagina": "Registrar Devolucao de EPI",
        },
    )
