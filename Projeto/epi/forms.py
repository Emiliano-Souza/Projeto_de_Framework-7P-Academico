from django import forms
from django.db.models import F
from django.utils import timezone

from epi.models import EPILote, EntregaEPI, Funcionario


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


class DevolucaoEPIForm(forms.Form):
    entrega = forms.ModelChoiceField(
        queryset=EntregaEPI.objects.none(),
        label="Entrega",
        empty_label="Selecione uma entrega pendente",
        help_text="Escolha uma entrega que ainda tenha itens para devolucao.",
    )
    quantidade_devolvida = forms.IntegerField(
        min_value=1,
        label="Quantidade devolvida",
        help_text="Informe quantas unidades estao retornando ao estoque.",
    )
    observacao = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Adicione detalhes uteis sobre a devolucao, se necessario.",
            }
        ),
        label="Observacao",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["entrega"].queryset = (
            EntregaEPI.objects.select_related("funcionario", "epi_lote", "epi_lote__epi")
            .filter(quantidade_devolvida__lt=F("quantidade_entregue"))
            .order_by("-data_entrega", "-id")
        )

        common_classes = "form-control"
        self.fields["entrega"].widget.attrs["class"] = common_classes
        self.fields["quantidade_devolvida"].widget.attrs["class"] = common_classes
        self.fields["observacao"].widget.attrs["class"] = common_classes


class BaixaEPIForm(forms.Form):
    MOTIVOS_BAIXA = [
        ("extraviado", "Extraviado"),
        ("danificado", "Danificado"),
        ("vencido", "Vencido"),
        ("descartado", "Descartado"),
    ]

    entrega = forms.ModelChoiceField(
        queryset=EntregaEPI.objects.none(),
        label="Entrega",
        empty_label="Selecione uma entrega com saldo em aberto",
        help_text="Escolha uma entrega que ainda tenha quantidade disponivel para baixa.",
    )
    quantidade_baixada = forms.IntegerField(
        min_value=1,
        label="Quantidade baixada",
        help_text="Informe quantas unidades serao encerradas sem retorno ao estoque.",
    )
    motivo_baixa = forms.ChoiceField(
        choices=MOTIVOS_BAIXA,
        label="Motivo da baixa",
        help_text="Selecione o motivo que justifica a baixa da quantidade informada.",
    )
    observacao = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Adicione detalhes uteis sobre a baixa, se necessario.",
            }
        ),
        label="Observacao",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["entrega"].queryset = (
            EntregaEPI.objects.select_related("funcionario", "epi_lote", "epi_lote__epi")
            .filter(quantidade_devolvida__lt=(F("quantidade_entregue") - F("quantidade_baixada")))
            .order_by("-data_entrega", "-id")
        )

        common_classes = "form-control"
        self.fields["entrega"].widget.attrs["class"] = common_classes
        self.fields["quantidade_baixada"].widget.attrs["class"] = common_classes
        self.fields["motivo_baixa"].widget.attrs["class"] = common_classes
        self.fields["observacao"].widget.attrs["class"] = common_classes
