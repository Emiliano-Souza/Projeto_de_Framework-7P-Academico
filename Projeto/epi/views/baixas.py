from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from epi.forms import BaixaEPIForm
from epi.services.entregas import registrar_baixa_epi
from epi.views.utils import aplicar_erros_ao_form


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
            aplicar_erros_ao_form(exc, form)
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
