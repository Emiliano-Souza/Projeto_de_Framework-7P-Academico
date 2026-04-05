from django.contrib import admin

from .models import Funcionario, Setor


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo", "created_at", "updated_at")
    list_filter = ("ativo",)
    search_fields = ("nome", "descricao")


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("matricula", "nome_completo", "setor", "cargo", "ativo")
    list_filter = ("ativo", "setor")
    search_fields = ("matricula", "nome_completo", "cargo")
