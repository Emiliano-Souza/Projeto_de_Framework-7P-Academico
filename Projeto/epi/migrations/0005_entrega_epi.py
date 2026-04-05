from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("epi", "0004_epi_lote"),
    ]

    operations = [
        migrations.CreateModel(
            name="EntregaEPI",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("quantidade_entregue", models.PositiveIntegerField()),
                ("quantidade_devolvida", models.PositiveIntegerField(default=0)),
                ("data_entrega", models.DateTimeField(db_index=True)),
                ("data_devolucao", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Entregue"),
                            (2, "Devolvido"),
                            (3, "Parcialmente devolvido"),
                            (4, "Extraviado"),
                            (5, "Danificado"),
                            (6, "Vencido"),
                        ],
                        default=1,
                    ),
                ),
                ("confirmado_recebimento", models.BooleanField(default=False)),
                ("observacao", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "epi_lote",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="entregas",
                        to="epi.epilote",
                    ),
                ),
                (
                    "funcionario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="entregas_epi",
                        to="epi.funcionario",
                    ),
                ),
                (
                    "usuario_devolucao",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="devolucoes_epi_registradas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "usuario_entrega",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="entregas_epi_registradas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "entrega_epi",
                "ordering": ["-data_entrega", "-id"],
                "verbose_name": "Entrega de EPI",
                "verbose_name_plural": "Entregas de EPI",
            },
        ),
        migrations.AddConstraint(
            model_name="entregaepi",
            constraint=models.CheckConstraint(
                condition=models.Q(quantidade_entregue__gt=0),
                name="ck_entrega_epi_quantidade_entregue_gt_0",
            ),
        ),
        migrations.AddConstraint(
            model_name="entregaepi",
            constraint=models.CheckConstraint(
                condition=models.Q(quantidade_devolvida__gte=0),
                name="ck_entrega_epi_quantidade_devolvida_gte_0",
            ),
        ),
        migrations.AddConstraint(
            model_name="entregaepi",
            constraint=models.CheckConstraint(
                condition=models.Q(quantidade_devolvida__lte=models.F("quantidade_entregue")),
                name="ck_entrega_epi_quantidade_devolvida_lte_entregue",
            ),
        ),
    ]
