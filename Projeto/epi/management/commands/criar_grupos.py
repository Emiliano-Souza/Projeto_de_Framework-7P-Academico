from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from epi.models import EPI, EPILote, EntregaEPI, Funcionario, MovimentacaoEstoque, Setor


GRUPOS = {
    "Administrador": None,  # todas as permissoes
    "Almoxarife": [
        "epi.view_setor",
        "epi.view_funcionario",
        "epi.view_epi",
        "epi.view_epilote",
        "epi.add_epilote",
        "epi.view_entregaepi",
        "epi.add_entregaepi",
        "epi.change_entregaepi",
        "epi.view_movimentacaoestoque",
    ],
    "Gestor": [
        "epi.view_setor",
        "epi.view_funcionario",
        "epi.view_epi",
        "epi.view_epilote",
        "epi.view_entregaepi",
        "epi.view_movimentacaoestoque",
    ],
}


class Command(BaseCommand):
    help = "Cria os grupos e permissoes do sistema"

    def handle(self, *args, **kwargs):
        for nome_grupo, codenames in GRUPOS.items():
            grupo, created = Group.objects.get_or_create(name=nome_grupo)

            if codenames is None:
                perms = Permission.objects.filter(
                    content_type__app_label="epi"
                )
                grupo.permissions.set(perms)
            else:
                perms = []
                for codename_completo in codenames:
                    app_label, codename = codename_completo.split(".")
                    try:
                        perm = Permission.objects.get(
                            codename=codename,
                            content_type__app_label=app_label,
                        )
                        perms.append(perm)
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"  Permissao nao encontrada: {codename_completo}")
                        )
                grupo.permissions.set(perms)

            status = "criado" if created else "atualizado"
            self.stdout.write(f"  Grupo '{nome_grupo}' {status}")

        self.stdout.write(self.style.SUCCESS("Grupos e permissoes configurados."))
