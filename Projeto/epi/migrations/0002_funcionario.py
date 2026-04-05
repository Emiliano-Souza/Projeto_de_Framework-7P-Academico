from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("epi", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Funcionario",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("matricula", models.CharField(max_length=20, unique=True)),
                ("nome_completo", models.CharField(db_index=True, max_length=150)),
                ("cargo", models.CharField(blank=True, max_length=100, null=True)),
                ("data_admissao", models.DateField(blank=True, null=True)),
                ("ativo", models.BooleanField(default=True)),
                ("observacao", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "setor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="funcionarios",
                        to="epi.setor",
                    ),
                ),
            ],
            options={
                "db_table": "funcionario",
                "ordering": ["nome_completo"],
                "verbose_name": "Funcionario",
                "verbose_name_plural": "Funcionarios",
            },
        ),
    ]
