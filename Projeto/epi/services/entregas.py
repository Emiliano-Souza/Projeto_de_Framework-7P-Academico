from django.core.exceptions import ValidationError
from django.utils import timezone

from epi.models import EntregaEPI


def _validar_funcionario_ativo(funcionario):
    if not funcionario.ativo:
        raise ValidationError({"funcionario": "O funcionario selecionado esta inativo."})


def _validar_lote_disponivel_para_entrega(epi_lote, quantidade_entregue, referencia=None):
    if epi_lote.data_validade and epi_lote.data_validade < referencia.date():
        raise ValidationError({"epi_lote": "O lote selecionado esta vencido."})

    if epi_lote.quantidade_disponivel < quantidade_entregue:
        raise ValidationError(
            {"quantidade_entregue": "Quantidade indisponivel no lote selecionado."}
        )


def registrar_entrega_epi(
    *,
    funcionario,
    epi_lote,
    quantidade_entregue,
    usuario_entrega,
    data_entrega=None,
    confirmado_recebimento=False,
    observacao=None,
):
    data_entrega = data_entrega or timezone.now()

    _validar_funcionario_ativo(funcionario)
    _validar_lote_disponivel_para_entrega(
        epi_lote,
        quantidade_entregue,
        referencia=data_entrega,
    )

    return EntregaEPI.objects.create(
        funcionario=funcionario,
        epi_lote=epi_lote,
        quantidade_entregue=quantidade_entregue,
        data_entrega=data_entrega,
        usuario_entrega=usuario_entrega,
        confirmado_recebimento=confirmado_recebimento,
        observacao=observacao,
    )
