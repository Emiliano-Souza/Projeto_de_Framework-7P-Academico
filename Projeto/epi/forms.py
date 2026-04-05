from django import forms
from django.utils import timezone

from epi.models import EPILote, Funcionario


class EntregaEPIForm(forms.Form):
    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.none(),
        label="Funcionario",
    )
    epi_lote = forms.ModelChoiceField(
        queryset=EPILote.objects.none(),
        label="Lote do EPI",
    )
    quantidade_entregue = forms.IntegerField(
        min_value=1,
        label="Quantidade",
    )
    data_entrega = forms.DateTimeField(
        initial=timezone.now,
        label="Data da entrega",
    )
    confirmado_recebimento = forms.BooleanField(
        required=False,
        label="Confirmado recebimento",
    )
    observacao = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Observacao",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["funcionario"].queryset = Funcionario.objects.filter(ativo=True).order_by(
            "nome_completo"
        )
        self.fields["epi_lote"].queryset = EPILote.objects.filter(
            quantidade_disponivel__gt=0
        ).order_by("data_validade", "numero_lote")
