from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone


class Setor(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "setor"
        ordering = ["nome"]
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    id = models.BigAutoField(primary_key=True)
    matricula = models.CharField(max_length=20, unique=True)
    nome_completo = models.CharField(max_length=150, db_index=True)
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        related_name="funcionarios",
    )
    cargo = models.CharField(max_length=100, null=True, blank=True)
    data_admissao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    observacao = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "funcionario"
        ordering = ["nome_completo"]
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"

    def __str__(self):
        return f"{self.nome_completo} ({self.matricula})"


class EPI(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo_interno = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=120, db_index=True)
    descricao = models.TextField(null=True, blank=True)
    categoria = models.CharField(max_length=50, null=True, blank=True)
    fabricante = models.CharField(max_length=100, null=True, blank=True)
    numero_ca = models.CharField(max_length=30, null=True, blank=True, db_index=True)
    controla_tamanho = models.BooleanField(default=False)
    estoque_minimo = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "epi"
        ordering = ["nome"]
        verbose_name = "EPI"
        verbose_name_plural = "EPIs"

    def __str__(self):
        return f"{self.codigo_interno} - {self.nome}"


class EPILote(models.Model):
    id = models.BigAutoField(primary_key=True)
    epi = models.ForeignKey(
        EPI,
        on_delete=models.PROTECT,
        related_name="lotes",
    )
    numero_lote = models.CharField(max_length=50)
    data_fabricacao = models.DateField(null=True, blank=True)
    data_validade = models.DateField(null=True, blank=True, db_index=True)
    quantidade_recebida = models.PositiveIntegerField()
    quantidade_disponivel = models.PositiveIntegerField()
    local_armazenamento = models.CharField(max_length=60, null=True, blank=True)
    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "epi_lote"
        ordering = ["data_validade", "numero_lote"]
        verbose_name = "Lote de EPI"
        verbose_name_plural = "Lotes de EPI"
        constraints = [
            models.UniqueConstraint(
                fields=["epi", "numero_lote"],
                name="uq_epi_lote_por_epi_numero_lote",
            ),
            models.CheckConstraint(
                condition=models.Q(quantidade_recebida__gt=0),
                name="ck_epi_lote_quantidade_recebida_gt_0",
            ),
            models.CheckConstraint(
                condition=models.Q(quantidade_disponivel__gte=0),
                name="ck_epi_lote_quantidade_disponivel_gte_0",
            ),
            models.CheckConstraint(
                condition=models.Q(quantidade_disponivel__lte=models.F("quantidade_recebida")),
                name="ck_epi_lote_quantidade_disponivel_lte_recebida",
            ),
        ]

    def clean(self):
        if self.quantidade_disponivel > self.quantidade_recebida:
            raise ValidationError(
                {
                    "quantidade_disponivel": (
                        "A quantidade disponivel nao pode ser maior que a quantidade recebida."
                    )
                }
            )

    def __str__(self):
        return f"{self.epi.nome} - lote {self.numero_lote}"


class EntregaEPI(models.Model):
    class Status(models.IntegerChoices):
        ENTREGUE = 1, "Entregue"
        DEVOLVIDO = 2, "Devolvido"
        PARCIALMENTE_DEVOLVIDO = 3, "Parcialmente devolvido"
        EXTRAVIADO = 4, "Extraviado"
        DANIFICADO = 5, "Danificado"
        VENCIDO = 6, "Vencido"

    id = models.BigAutoField(primary_key=True)
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name="entregas_epi",
    )
    epi_lote = models.ForeignKey(
        EPILote,
        on_delete=models.PROTECT,
        related_name="entregas",
    )
    quantidade_entregue = models.PositiveIntegerField()
    quantidade_devolvida = models.PositiveIntegerField(default=0)
    data_entrega = models.DateTimeField(db_index=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.ENTREGUE,
    )
    confirmado_recebimento = models.BooleanField(default=False)
    usuario_entrega = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="entregas_epi_registradas",
    )
    usuario_devolucao = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="devolucoes_epi_registradas",
        null=True,
        blank=True,
    )
    observacao = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "entrega_epi"
        ordering = ["-data_entrega", "-id"]
        verbose_name = "Entrega de EPI"
        verbose_name_plural = "Entregas de EPI"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantidade_entregue__gt=0),
                name="ck_entrega_epi_quantidade_entregue_gt_0",
            ),
            models.CheckConstraint(
                condition=models.Q(quantidade_devolvida__gte=0),
                name="ck_entrega_epi_quantidade_devolvida_gte_0",
            ),
            models.CheckConstraint(
                condition=models.Q(quantidade_devolvida__lte=models.F("quantidade_entregue")),
                name="ck_entrega_epi_quantidade_devolvida_lte_entregue",
            ),
        ]

    def clean(self):
        errors = {}

        if self.quantidade_devolvida > 0:
            if not self.usuario_devolucao_id:
                errors["usuario_devolucao"] = "Informe o usuario da devolucao."
        else:
            self.data_devolucao = None
            self.usuario_devolucao = None

        if self.quantidade_devolvida == 0 and self.status == self.Status.DEVOLVIDO:
            self.status = self.Status.ENTREGUE

        if self.quantidade_devolvida == self.quantidade_entregue:
            self.status = self.Status.DEVOLVIDO
        elif self.quantidade_devolvida > 0:
            self.status = self.Status.PARCIALMENTE_DEVOLVIDO
        elif self.status in {
            self.Status.DEVOLVIDO,
            self.Status.PARCIALMENTE_DEVOLVIDO,
        }:
            self.status = self.Status.ENTREGUE

        if self.pk:
            entrega_anterior = (
                EntregaEPI.objects.filter(pk=self.pk)
                .values("quantidade_entregue", "quantidade_devolvida")
                .first()
            )
            if entrega_anterior:
                if self.quantidade_entregue < entrega_anterior["quantidade_entregue"]:
                    errors["quantidade_entregue"] = (
                        "Nao e permitido reduzir a quantidade entregue apos o registro."
                    )
                if self.quantidade_devolvida < entrega_anterior["quantidade_devolvida"]:
                    errors["quantidade_devolvida"] = (
                        "Nao e permitido reduzir a quantidade devolvida apos o registro."
                    )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()

        with transaction.atomic():
            lote = EPILote.objects.select_for_update().get(pk=self.epi_lote_id)
            saldo_inicial = lote.quantidade_disponivel
            entrega_anterior = None

            if self.pk:
                entrega_anterior = (
                    EntregaEPI.objects.select_for_update()
                    .filter(pk=self.pk)
                    .first()
                )

            quantidade_entregue_anterior = 0
            quantidade_devolvida_anterior = 0
            if entrega_anterior:
                quantidade_entregue_anterior = entrega_anterior.quantidade_entregue
                quantidade_devolvida_anterior = entrega_anterior.quantidade_devolvida

            delta_entrega = self.quantidade_entregue - quantidade_entregue_anterior
            delta_devolucao = self.quantidade_devolvida - quantidade_devolvida_anterior
            novo_saldo = lote.quantidade_disponivel - delta_entrega + delta_devolucao

            if novo_saldo < 0:
                raise ValidationError(
                    {"quantidade_entregue": "Quantidade indisponivel no lote selecionado."}
                )

            lote.quantidade_disponivel = novo_saldo
            lote.save(update_fields=["quantidade_disponivel", "updated_at"])

            if self.quantidade_devolvida > 0 and not self.data_devolucao:
                self.data_devolucao = timezone.now()

            super().save(*args, **kwargs)

            saldo_cursor = saldo_inicial
            if delta_entrega > 0:
                MovimentacaoEstoque.objects.create(
                    epi_lote=lote,
                    tipo_movimento=MovimentacaoEstoque.TipoMovimento.ENTREGA,
                    quantidade=delta_entrega,
                    quantidade_antes=saldo_cursor,
                    quantidade_depois=saldo_cursor - delta_entrega,
                    funcionario=self.funcionario,
                    entrega_epi=self,
                    usuario=self.usuario_entrega,
                    motivo="Entrega de EPI",
                    observacao=self.observacao,
                )
                saldo_cursor -= delta_entrega

            if delta_devolucao > 0:
                MovimentacaoEstoque.objects.create(
                    epi_lote=lote,
                    tipo_movimento=MovimentacaoEstoque.TipoMovimento.DEVOLUCAO,
                    quantidade=delta_devolucao,
                    quantidade_antes=saldo_cursor,
                    quantidade_depois=saldo_cursor + delta_devolucao,
                    funcionario=self.funcionario,
                    entrega_epi=self,
                    usuario=self.usuario_devolucao,
                    motivo="Devolucao de EPI",
                    observacao=self.observacao,
                )
                saldo_cursor += delta_devolucao

    def __str__(self):
        return f"{self.funcionario.nome_completo} - {self.epi_lote.epi.nome}"


class MovimentacaoEstoque(models.Model):
    class TipoMovimento(models.IntegerChoices):
        ENTRADA = 1, "Entrada"
        ENTREGA = 2, "Entrega"
        DEVOLUCAO = 3, "Devolucao"
        AJUSTE = 4, "Ajuste"
        DESCARTE = 5, "Descarte"
        PERDA = 6, "Perda"

    id = models.BigAutoField(primary_key=True)
    epi_lote = models.ForeignKey(
        EPILote,
        on_delete=models.PROTECT,
        related_name="movimentacoes_estoque",
    )
    tipo_movimento = models.PositiveSmallIntegerField(choices=TipoMovimento.choices)
    quantidade = models.PositiveIntegerField()
    quantidade_antes = models.PositiveIntegerField()
    quantidade_depois = models.PositiveIntegerField()
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name="movimentacoes_estoque",
        null=True,
        blank=True,
    )
    entrega_epi = models.ForeignKey(
        EntregaEPI,
        on_delete=models.PROTECT,
        related_name="movimentacoes_estoque",
        null=True,
        blank=True,
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="movimentacoes_estoque_registradas",
    )
    motivo = models.CharField(max_length=100, null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "movimentacao_estoque"
        ordering = ["-created_at", "-id"]
        verbose_name = "Movimentacao de Estoque"
        verbose_name_plural = "Movimentacoes de Estoque"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantidade__gt=0),
                name="ck_mov_estoque_quantidade_gt_0",
            ),
            models.CheckConstraint(
                condition=models.Q(quantidade_antes__gte=0),
                name="ck_mov_estoque_quantidade_antes_gte_0",
            ),
            models.CheckConstraint(
                condition=models.Q(quantidade_depois__gte=0),
                name="ck_mov_estoque_quantidade_depois_gte_0",
            ),
        ]

    def __str__(self):
        return f"{self.get_tipo_movimento_display()} - {self.epi_lote.numero_lote}"
