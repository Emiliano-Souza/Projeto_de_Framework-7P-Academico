from django import forms
from django.utils import timezone

from epi.models import EPILote, Funcionario


class EntregaEPIForm(forms.Form):
    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.none(),
        label="Funcionário",
        empty_label="Selecione um funcionário",
    )
    epi_lote = forms.ModelChoiceField(
        queryset=EPILote.objects.none(),
        label="Lote do EPI",
        empty_label="Selecione um lote disponível",
    )
    quantidade_entregue = forms.IntegerField(
        min_value=1,
        label="Quantidade",
        help_text="Informe quantas unidades serão entregues.",
    )
    data_entrega = forms.DateTimeField(
        initial=timezone.now,
        label="Data da entrega",
        input_formats=["%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"],
        help_text="Use o formato AAAA-MM-DD HH:MM ou DD/MM/AAAA HH:MM.",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            },
            format="%Y-%m-%dT%H:%M",
        ),
    )
    confirmado_recebimento = forms.BooleanField(
        required=False,
        label="Recebimento confirmado",
    )
    observacao = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Adicione detalhes úteis sobre a entrega, se necessário.",
            }
        ),
        label="Observação",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["funcionario"].queryset = Funcionario.objects.filter(ativo=True).order_by(
            "nome_completo"
        )
        self.fields["epi_lote"].queryset = EPILote.objects.filter(
            quantidade_disponivel__gt=0
        ).order_by("data_validade", "numero_lote")

        common_classes = "form-control"
        checkbox_classes = "form-checkbox"

        for field_name in ("funcionario", "epi_lote", "quantidade_entregue", "data_entrega"):
            self.fields[field_name].widget.attrs["class"] = common_classes

        self.fields["observacao"].widget.attrs["class"] = common_classes
        self.fields["confirmado_recebimento"].widget.attrs["class"] = checkbox_classes
