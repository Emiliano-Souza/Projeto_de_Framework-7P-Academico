from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("epi", "0002_funcionario"),
    ]

    operations = [
        migrations.CreateModel(
            name="EPI",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("codigo_interno", models.CharField(max_length=30, unique=True)),
                ("nome", models.CharField(db_index=True, max_length=120)),
                ("descricao", models.TextField(blank=True, null=True)),
                ("categoria", models.CharField(blank=True, max_length=50, null=True)),
                ("fabricante", models.CharField(blank=True, max_length=100, null=True)),
                ("numero_ca", models.CharField(blank=True, db_index=True, max_length=30, null=True)),
                ("controla_tamanho", models.BooleanField(default=False)),
                ("estoque_minimo", models.PositiveIntegerField(default=0)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "epi",
                "ordering": ["nome"],
                "verbose_name": "EPI",
                "verbose_name_plural": "EPIs",
            },
        ),
    ]
