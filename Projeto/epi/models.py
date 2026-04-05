from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


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
    quantidade_baixada = models.PositiveIntegerField(default=0)
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
            models.CheckConstraint(
                condition=(
                    models.Q(
                        quantidade_devolvida__lte=(
                            models.F("quantidade_entregue") - models.F("quantidade_baixada")
                        )
                    )
                ),
                name="ck_entrega_epi_devolvida_mais_baixada_lte_entregue",
            ),
        ]

    def clean(self):
        if self.quantidade_devolvida > 0 and not self.usuario_devolucao_id:
            raise ValidationError({"usuario_devolucao": "Informe o usuario da devolucao."})

        if self.quantidade_devolvida + self.quantidade_baixada > self.quantidade_entregue:
            raise ValidationError(
                {
                    "quantidade_baixada": (
                        "A soma de devolucao e baixa nao pode ser maior que a quantidade entregue."
                    )
                }
            )

    def save(self, *args, **kwargs):
        from epi.services.entregas import persistir_entrega_epi

        return persistir_entrega_epi(self, *args, **kwargs)

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
        BAIXA = 7, "Baixa"

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
