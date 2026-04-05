from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("epi", "0005_entrega_epi"),
    ]

    operations = [
        migrations.CreateModel(
            name="MovimentacaoEstoque",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "tipo_movimento",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Entrada"),
                            (2, "Entrega"),
                            (3, "Devolucao"),
                            (4, "Ajuste"),
                            (5, "Descarte"),
                            (6, "Perda"),
                        ]
                    ),
                ),
                ("quantidade", models.PositiveIntegerField()),
                ("quantidade_antes", models.PositiveIntegerField()),
                ("quantidade_depois", models.PositiveIntegerField()),
                ("motivo", models.CharField(blank=True, max_length=100, null=True)),
                ("observacao", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "entrega_epi",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movimentacoes_estoque",
                        to="epi.entregaepi",
                    ),
                ),
                (
                    "epi_lote",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movimentacoes_estoque",
                        to="epi.epilote",
                    ),
                ),
                (
                    "funcionario",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movimentacoes_estoque",
                        to="epi.funcionario",
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movimentacoes_estoque_registradas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "movimentacao_estoque",
                "ordering": ["-created_at", "-id"],
                "verbose_name": "Movimentacao de Estoque",
                "verbose_name_plural": "Movimentacoes de Estoque",
            },
        ),
        migrations.AddConstraint(
            model_name="movimentacaoestoque",
            constraint=models.CheckConstraint(
                condition=models.Q(quantidade__gt=0),
                name="ck_mov_estoque_quantidade_gt_0",
            ),
        ),
        migrations.AddConstraint(
            model_name="movimentacaoestoque",
            constraint=models.CheckConstraint(
                condition=models.Q(quantidade_antes__gte=0),
                name="ck_mov_estoque_quantidade_antes_gte_0",
            ),
        ),
        migrations.AddConstraint(
            model_name="movimentacaoestoque",
            constraint=models.CheckConstraint(
                condition=models.Q(quantidade_depois__gte=0),
                name="ck_mov_estoque_quantidade_depois_gte_0",
            ),
        ),
    ]
