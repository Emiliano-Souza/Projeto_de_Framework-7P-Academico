from django.core.exceptions import ValidationError

from epi.models import EPILote
from epi.tests.base import BaseModelTestCase


class EPILoteModelTests(BaseModelTestCase):
    def test_nao_permite_quantidade_disponivel_maior_que_recebida(self):
        lote = EPILote(
            epi=self.epi,
            numero_lote="L002",
            quantidade_recebida=5,
            quantidade_disponivel=6,
        )

        with self.assertRaises(ValidationError):
            lote.full_clean()

    def test_nao_permite_lote_duplicado_para_mesmo_epi(self):
        lote = EPILote(
            epi=self.epi,
            numero_lote="L001",
            quantidade_recebida=5,
            quantidade_disponivel=5,
        )

        with self.assertRaises(ValidationError):
            lote.full_clean()

    def test_nao_permite_quantidade_recebida_menor_ou_igual_a_zero(self):
        lote = EPILote(
            epi=self.epi,
            numero_lote="L003",
            quantidade_recebida=0,
            quantidade_disponivel=0,
        )

        with self.assertRaises(ValidationError):
            lote.full_clean()
