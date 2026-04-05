from django.core.exceptions import ValidationError
from django.db import transaction

from epi.models import EPILote, MovimentacaoEstoque


def registrar_entrada_lote(
    *,
    epi,
    numero_lote,
    quantidade_recebida,
    usuario_responsavel,
    data_fabricacao=None,
    data_validade=None,
    local_armazenamento=None,
    valor_unitario=None,
    observacao=None,
):
    if quantidade_recebida <= 0:
        raise ValidationError(
            {"quantidade_recebida": "Informe uma quantidade recebida maior que zero."}
        )

    with transaction.atomic():
        lote = EPILote(
            epi=epi,
            numero_lote=numero_lote,
            data_fabricacao=data_fabricacao,
            data_validade=data_validade,
            quantidade_recebida=quantidade_recebida,
            quantidade_disponivel=quantidade_recebida,
            local_armazenamento=local_armazenamento,
            valor_unitario=valor_unitario,
        )
        lote.full_clean()
        lote.save()

        MovimentacaoEstoque.objects.create(
            epi_lote=lote,
            tipo_movimento=MovimentacaoEstoque.TipoMovimento.ENTRADA,
            quantidade=quantidade_recebida,
            quantidade_antes=0,
            quantidade_depois=quantidade_recebida,
            usuario=usuario_responsavel,
            motivo="Entrada de lote",
            observacao=observacao,
        )

    return lote
