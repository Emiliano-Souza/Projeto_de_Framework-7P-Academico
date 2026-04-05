from django.core.exceptions import ValidationError

from epi.models import EPILote, MovimentacaoEstoque
from epi.services.lotes import registrar_entrada_lote
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


class EPILoteServiceTests(BaseModelTestCase):
    def test_service_registra_entrada_de_lote_com_movimentacao(self):
        lote = registrar_entrada_lote(
            epi=self.epi,
            numero_lote="L100",
            quantidade_recebida=12,
            usuario_responsavel=self.user,
            observacao="Entrada inicial de estoque",
        )

        movimentacao = MovimentacaoEstoque.objects.get(
            epi_lote=lote,
            tipo_movimento=MovimentacaoEstoque.TipoMovimento.ENTRADA,
        )

        self.assertEqual(lote.quantidade_recebida, 12)
        self.assertEqual(lote.quantidade_disponivel, 12)
        self.assertEqual(movimentacao.quantidade, 12)
        self.assertEqual(movimentacao.quantidade_antes, 0)
        self.assertEqual(movimentacao.quantidade_depois, 12)
        self.assertEqual(movimentacao.usuario, self.user)

    def test_service_bloqueia_entrada_com_quantidade_invalida(self):
        with self.assertRaises(ValidationError):
            registrar_entrada_lote(
                epi=self.epi,
                numero_lote="L101",
                quantidade_recebida=0,
                usuario_responsavel=self.user,
            )

    def test_service_bloqueia_lote_duplicado(self):
        with self.assertRaises(ValidationError):
            registrar_entrada_lote(
                epi=self.epi,
                numero_lote="L001",
                quantidade_recebida=5,
                usuario_responsavel=self.user,
            )

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
