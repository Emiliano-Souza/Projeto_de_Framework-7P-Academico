from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("epi", "0007_lote_disponivel_e_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="entregaepi",
            name="quantidade_baixada",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RemoveConstraint(
            model_name="entregaepi",
            name="ck_entrega_epi_quantidade_devolvida_lte_entregue",
        ),
        migrations.AddConstraint(
            model_name="entregaepi",
            constraint=models.CheckConstraint(
                condition=models.Q(quantidade_devolvida__lte=models.F("quantidade_entregue")),
                name="ck_entrega_epi_quantidade_devolvida_lte_entregue",
            ),
        ),
        migrations.AddConstraint(
            model_name="entregaepi",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    quantidade_devolvida__lte=(
                        models.F("quantidade_entregue") - models.F("quantidade_baixada")
                    )
                ),
                name="ck_entrega_epi_devolvida_mais_baixada_lte_entregue",
            ),
        ),
        migrations.AlterField(
            model_name="movimentacaoestoque",
            name="tipo_movimento",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "Entrada"),
                    (2, "Entrega"),
                    (3, "Devolucao"),
                    (4, "Ajuste"),
                    (5, "Descarte"),
                    (6, "Perda"),
                    (7, "Baixa"),
                ]
            ),
        ),
    ]
