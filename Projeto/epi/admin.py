from django.contrib import admin

from .models import EPI, EPILote, Funcionario, Setor


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


@admin.register(EPI)
class EPIAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_interno",
        "nome",
        "categoria",
        "numero_ca",
        "estoque_minimo",
        "ativo",
    )
    list_filter = ("ativo", "controla_tamanho", "categoria")
    search_fields = ("codigo_interno", "nome", "numero_ca", "fabricante")


@admin.register(EPILote)
class EPILoteAdmin(admin.ModelAdmin):
    list_display = (
        "epi",
        "numero_lote",
        "data_validade",
        "quantidade_recebida",
        "quantidade_disponivel",
    )
    list_filter = ("data_validade", "epi")
    search_fields = ("numero_lote", "epi__codigo_interno", "epi__nome")
