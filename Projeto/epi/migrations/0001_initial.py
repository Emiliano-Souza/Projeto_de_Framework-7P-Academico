from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Setor",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=100, unique=True)),
                ("descricao", models.CharField(blank=True, max_length=255, null=True)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "setor",
                "ordering": ["nome"],
                "verbose_name": "Setor",
                "verbose_name_plural": "Setores",
            },
        ),
    ]
