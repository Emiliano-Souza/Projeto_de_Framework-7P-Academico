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
