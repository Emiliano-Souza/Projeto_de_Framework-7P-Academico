from django.contrib import admin

from .models import Setor


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo", "created_at", "updated_at")
    list_filter = ("ativo",)
    search_fields = ("nome", "descricao")
