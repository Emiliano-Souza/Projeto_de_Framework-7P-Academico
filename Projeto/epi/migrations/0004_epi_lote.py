from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("epi", "0003_epi"),
    ]

    operations = [
        migrations.CreateModel(
            name="EPILote",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("numero_lote", models.CharField(max_length=50)),
                ("data_fabricacao", models.DateField(blank=True, null=True)),
                ("data_validade", models.DateField(blank=True, db_index=True, null=True)),
                ("quantidade_recebida", models.PositiveIntegerField()),
                ("quantidade_disponivel", models.PositiveIntegerField()),
                ("local_armazenamento", models.CharField(blank=True, max_length=60, null=True)),
                ("valor_unitario", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "epi",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="lotes",
                        to="epi.epi",
                    ),
                ),
            ],
            options={
                "db_table": "epi_lote",
                "ordering": ["data_validade", "numero_lote"],
                "verbose_name": "Lote de EPI",
                "verbose_name_plural": "Lotes de EPI",
            },
        ),
        migrations.AddConstraint(
            model_name="epilote",
            constraint=models.UniqueConstraint(
                fields=("epi", "numero_lote"),
                name="uq_epi_lote_por_epi_numero_lote",
            ),
        ),
        migrations.AddConstraint(
            model_name="epilote",
            constraint=models.CheckConstraint(
                condition=models.Q(quantidade_recebida__gt=0),
                name="ck_epi_lote_quantidade_recebida_gt_0",
            ),
        ),
        migrations.AddConstraint(
            model_name="epilote",
            constraint=models.CheckConstraint(
                condition=models.Q(quantidade_disponivel__gte=0),
                name="ck_epi_lote_quantidade_disponivel_gte_0",
            ),
        ),
    ]
