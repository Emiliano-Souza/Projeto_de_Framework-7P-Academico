from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from epi.models import EPILote, EntregaEPI, MovimentacaoEstoque


def _validar_funcionario_ativo(funcionario):
    if not funcionario.ativo:
        raise ValidationError({"funcionario": "O funcionario selecionado esta inativo."})


def _ajustar_status_e_campos_de_devolucao(entrega):
    if entrega.quantidade_devolvida > 0:
        if not entrega.usuario_devolucao_id:
            raise ValidationError({"usuario_devolucao": "Informe o usuario da devolucao."})
        if not entrega.data_devolucao:
            entrega.data_devolucao = timezone.now()
    else:
        entrega.data_devolucao = None
        entrega.usuario_devolucao = None

    if entrega.quantidade_devolvida == entrega.quantidade_entregue:
        entrega.status = EntregaEPI.Status.DEVOLVIDO
    elif entrega.quantidade_devolvida > 0:
        entrega.status = EntregaEPI.Status.PARCIALMENTE_DEVOLVIDO
    elif entrega.status in {
        EntregaEPI.Status.DEVOLVIDO,
        EntregaEPI.Status.PARCIALMENTE_DEVOLVIDO,
    }:
        entrega.status = EntregaEPI.Status.ENTREGUE


def _saldo_aberto_da_entrega(entrega):
    return entrega.quantidade_entregue - entrega.quantidade_devolvida - entrega.quantidade_baixada


def _validar_reducao_retroativa(entrega, entrega_anterior):
    errors = {}

    if entrega_anterior:
        if entrega.quantidade_entregue < entrega_anterior.quantidade_entregue:
            errors["quantidade_entregue"] = (
                "Nao e permitido reduzir a quantidade entregue apos o registro."
            )
        if entrega.quantidade_devolvida < entrega_anterior.quantidade_devolvida:
            errors["quantidade_devolvida"] = (
                "Nao e permitido reduzir a quantidade devolvida apos o registro."
            )
        if entrega.quantidade_baixada < entrega_anterior.quantidade_baixada:
            errors["quantidade_baixada"] = (
                "Nao e permitido reduzir a quantidade baixada apos o registro."
            )

    if errors:
        raise ValidationError(errors)


def persistir_entrega_epi(entrega, *args, **kwargs):
    with transaction.atomic():
        lote = EPILote.objects.select_for_update().get(pk=entrega.epi_lote_id)
        saldo_inicial = lote.quantidade_disponivel
        entrega_anterior = None

        if entrega.pk:
            entrega_anterior = (
                EntregaEPI.objects.select_for_update()
                .filter(pk=entrega.pk)
                .first()
            )

        _ajustar_status_e_campos_de_devolucao(entrega)
        _validar_reducao_retroativa(entrega, entrega_anterior)
        entrega.full_clean()

        quantidade_entregue_anterior = 0
        quantidade_devolvida_anterior = 0
        quantidade_baixada_anterior = 0
        if entrega_anterior:
            quantidade_entregue_anterior = entrega_anterior.quantidade_entregue
            quantidade_devolvida_anterior = entrega_anterior.quantidade_devolvida
            quantidade_baixada_anterior = entrega_anterior.quantidade_baixada

        delta_entrega = entrega.quantidade_entregue - quantidade_entregue_anterior
        delta_devolucao = entrega.quantidade_devolvida - quantidade_devolvida_anterior
        delta_baixa = entrega.quantidade_baixada - quantidade_baixada_anterior
        novo_saldo = lote.quantidade_disponivel - delta_entrega + delta_devolucao

        if novo_saldo < 0:
            raise ValidationError(
                {"quantidade_entregue": "Quantidade indisponivel no lote selecionado."}
            )

        lote.quantidade_disponivel = novo_saldo
        lote.save(update_fields=["quantidade_disponivel", "updated_at"])

        super(EntregaEPI, entrega).save(*args, **kwargs)

        saldo_cursor = saldo_inicial
        if delta_entrega > 0:
            MovimentacaoEstoque.objects.create(
                epi_lote=lote,
                tipo_movimento=MovimentacaoEstoque.TipoMovimento.ENTREGA,
                quantidade=delta_entrega,
                quantidade_antes=saldo_cursor,
                quantidade_depois=saldo_cursor - delta_entrega,
                funcionario=entrega.funcionario,
                entrega_epi=entrega,
                usuario=entrega.usuario_entrega,
                motivo="Entrega de EPI",
                observacao=entrega.observacao,
            )
            saldo_cursor -= delta_entrega

        if delta_devolucao > 0:
            MovimentacaoEstoque.objects.create(
                epi_lote=lote,
                tipo_movimento=MovimentacaoEstoque.TipoMovimento.DEVOLUCAO,
                quantidade=delta_devolucao,
                quantidade_antes=saldo_cursor,
                quantidade_depois=saldo_cursor + delta_devolucao,
                funcionario=entrega.funcionario,
                entrega_epi=entrega,
                usuario=entrega.usuario_devolucao,
                motivo="Devolucao de EPI",
                observacao=entrega.observacao,
            )

        if delta_baixa > 0:
            MovimentacaoEstoque.objects.create(
                epi_lote=lote,
                tipo_movimento=MovimentacaoEstoque.TipoMovimento.BAIXA,
                quantidade=delta_baixa,
                quantidade_antes=saldo_cursor,
                quantidade_depois=saldo_cursor,
                funcionario=entrega.funcionario,
                entrega_epi=entrega,
                usuario=entrega.usuario_devolucao or entrega.usuario_entrega,
                motivo="Baixa de EPI",
                observacao=entrega.observacao,
            )

    return entrega


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

    entrega = EntregaEPI(
        funcionario=funcionario,
        epi_lote=epi_lote,
        quantidade_entregue=quantidade_entregue,
        data_entrega=data_entrega,
        usuario_entrega=usuario_entrega,
        confirmado_recebimento=confirmado_recebimento,
        observacao=observacao,
    )
    return persistir_entrega_epi(entrega)


def registrar_devolucao_epi(
    *,
    entrega_id,
    quantidade_devolvida,
    usuario_devolucao,
    observacao=None,
    data_devolucao=None,
):
    if quantidade_devolvida <= 0:
        raise ValidationError(
            {"quantidade_devolvida": "Informe uma quantidade devolvida maior que zero."}
        )

    try:
        entrega = EntregaEPI.objects.select_related("funcionario", "epi_lote", "epi_lote__epi").get(
            pk=entrega_id
        )
    except EntregaEPI.DoesNotExist as exc:
        raise ValidationError({"entrega": "A entrega informada nao existe."}) from exc

    saldo_devolvivel = entrega.quantidade_entregue - entrega.quantidade_devolvida
    if quantidade_devolvida > saldo_devolvivel:
        raise ValidationError(
            {
                "quantidade_devolvida": (
                    "A quantidade devolvida nao pode ser maior que o saldo pendente da entrega."
                )
            }
        )

    entrega.quantidade_devolvida += quantidade_devolvida
    entrega.usuario_devolucao = usuario_devolucao
    entrega.data_devolucao = data_devolucao or timezone.now()
    if observacao:
        entrega.observacao = observacao

    return persistir_entrega_epi(entrega)


def registrar_baixa_epi(
    *,
    entrega_id,
    quantidade_baixada,
    usuario_baixa,
    motivo_baixa,
    observacao=None,
):
    if quantidade_baixada <= 0:
        raise ValidationError(
            {"quantidade_baixada": "Informe uma quantidade baixada maior que zero."}
        )

    if not motivo_baixa:
        raise ValidationError({"motivo_baixa": "Informe o motivo da baixa."})

    try:
        entrega = EntregaEPI.objects.select_related("funcionario", "epi_lote", "epi_lote__epi").get(
            pk=entrega_id
        )
    except EntregaEPI.DoesNotExist as exc:
        raise ValidationError({"entrega": "A entrega informada nao existe."}) from exc

    saldo_aberto = _saldo_aberto_da_entrega(entrega)
    if quantidade_baixada > saldo_aberto:
        raise ValidationError(
            {
                "quantidade_baixada": (
                    "A quantidade baixada nao pode ser maior que o saldo em aberto da entrega."
                )
            }
        )

    entrega.quantidade_baixada += quantidade_baixada
    entrega.usuario_devolucao = usuario_baixa

    if observacao:
        entrega.observacao = f"[{motivo_baixa}] {observacao}"
    else:
        entrega.observacao = f"[{motivo_baixa}]"

    return persistir_entrega_epi(entrega)
