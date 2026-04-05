from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from epi.models import EPI, EntregaEPI, Funcionario, Setor
from epi.tests.base import BaseModelTestCase
from django.utils import timezone


class CadastroModelTests(BaseModelTestCase):
    def test_nao_permite_nome_de_setor_duplicado(self):
        setor = Setor(nome="Producao")

        with self.assertRaises(ValidationError):
            setor.full_clean()

    def test_nao_permite_matricula_duplicada(self):
        funcionario = Funcionario(
            matricula="F001",
            nome_completo="Joao Pereira",
            setor=self.setor,
        )

        with self.assertRaises(ValidationError):
            funcionario.full_clean()

    def test_nao_permite_codigo_interno_duplicado(self):
        epi = EPI(
            codigo_interno="EPI-001",
            nome="Luva de Seguranca",
        )

        with self.assertRaises(ValidationError):
            epi.full_clean()

    def test_protect_impede_excluir_setor_com_funcionario(self):
        with self.assertRaises(ProtectedError):
            self.setor.delete()

    def test_protect_impede_excluir_lote_com_entrega(self):
        EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=1,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )

        with self.assertRaises(ProtectedError):
            self.lote.delete()
