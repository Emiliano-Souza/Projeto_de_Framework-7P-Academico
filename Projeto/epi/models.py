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
