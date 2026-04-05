from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("epi", "0006_movimentacao_estoque"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="epilote",
            constraint=models.CheckConstraint(
                condition=models.Q(quantidade_disponivel__lte=models.F("quantidade_recebida")),
                name="ck_epi_lote_quantidade_disponivel_lte_recebida",
            ),
        ),
    ]
