from django.contrib.auth import get_user_model
from django.test import TestCase

from epi.models import EPI, EPILote, Funcionario, Setor


class BaseModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="senha-forte-123",
        )
        self.setor = Setor.objects.create(nome="Producao")
        self.funcionario = Funcionario.objects.create(
            matricula="F001",
            nome_completo="Maria da Silva",
            setor=self.setor,
        )
        self.epi = EPI.objects.create(
            codigo_interno="EPI-001",
            nome="Capacete de Seguranca",
            numero_ca="12345",
        )
        self.lote = EPILote.objects.create(
            epi=self.epi,
            numero_lote="L001",
            quantidade_recebida=10,
            quantidade_disponivel=10,
        )
