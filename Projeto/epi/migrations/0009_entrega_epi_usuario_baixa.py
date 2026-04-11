import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("epi", "0008_entrega_epi_baixa_estrutura"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="entregaepi",
            name="usuario_baixa",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="baixas_epi_registradas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
