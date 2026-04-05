from django.contrib import admin

from .models import EPI, EPILote, EntregaEPI, Funcionario, MovimentacaoEstoque, Setor


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


@admin.register(EntregaEPI)
class EntregaEPIAdmin(admin.ModelAdmin):
    list_display = (
        "funcionario",
        "epi_lote",
        "quantidade_entregue",
        "quantidade_devolvida",
        "status",
        "data_entrega",
    )
    list_filter = ("status", "confirmado_recebimento", "data_entrega")
    search_fields = (
        "funcionario__matricula",
        "funcionario__nome_completo",
        "epi_lote__numero_lote",
        "epi_lote__epi__nome",
    )


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        "tipo_movimento",
        "epi_lote",
        "quantidade",
        "quantidade_antes",
        "quantidade_depois",
        "created_at",
    )
    list_filter = ("tipo_movimento", "created_at")
    search_fields = (
        "epi_lote__numero_lote",
        "epi_lote__epi__nome",
        "funcionario__nome_completo",
        "motivo",
    )
