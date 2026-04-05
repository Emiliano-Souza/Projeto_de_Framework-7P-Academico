from django.core.exceptions import ValidationError

from epi.models import MovimentacaoEstoque
from epi.tests.base import BaseModelTestCase


class MovimentacaoEstoqueModelTests(BaseModelTestCase):
    def test_tipo_movimento_baixa_esta_disponivel(self):
        self.assertEqual(MovimentacaoEstoque.TipoMovimento.BAIXA, 7)

    def test_nao_permite_movimentacao_com_quantidade_zero(self):
        movimentacao = MovimentacaoEstoque(
            epi_lote=self.lote,
            tipo_movimento=MovimentacaoEstoque.TipoMovimento.AJUSTE,
            quantidade=0,
            quantidade_antes=10,
            quantidade_depois=10,
            usuario=self.user,
        )

        with self.assertRaises(ValidationError):
            movimentacao.full_clean()

    def test_nao_permite_movimentacao_com_saldo_negativo(self):
        movimentacao = MovimentacaoEstoque(
            epi_lote=self.lote,
            tipo_movimento=MovimentacaoEstoque.TipoMovimento.AJUSTE,
            quantidade=1,
            quantidade_antes=0,
            quantidade_depois=-1,
            usuario=self.user,
        )

        with self.assertRaises(ValidationError):
            movimentacao.full_clean()
