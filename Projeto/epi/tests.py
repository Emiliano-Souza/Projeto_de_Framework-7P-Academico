from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.test import TestCase
from django.utils import timezone

from .models import EPI, EPILote, EntregaEPI, Funcionario, MovimentacaoEstoque, Setor


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


class EntregaEPIModelTests(BaseModelTestCase):
    def test_entrega_baixa_saldo_do_lote_e_gera_movimentacao(self):
        entrega = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=3,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )

        self.lote.refresh_from_db()
        movimentacao = MovimentacaoEstoque.objects.get(entrega_epi=entrega)

        self.assertEqual(self.lote.quantidade_disponivel, 7)
        self.assertEqual(movimentacao.tipo_movimento, MovimentacaoEstoque.TipoMovimento.ENTREGA)
        self.assertEqual(movimentacao.quantidade_antes, 10)
        self.assertEqual(movimentacao.quantidade_depois, 7)
        self.assertEqual(entrega.status, EntregaEPI.Status.ENTREGUE)

    def test_devolucao_retorna_saldo_gera_movimentacao_e_ajusta_status(self):
        entrega = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=4,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )

        entrega.quantidade_devolvida = 2
        entrega.usuario_devolucao = self.user
        entrega.save()

        self.lote.refresh_from_db()
        entrega.refresh_from_db()
        movimentacoes = MovimentacaoEstoque.objects.filter(entrega_epi=entrega).order_by("id")

        self.assertEqual(self.lote.quantidade_disponivel, 8)
        self.assertEqual(movimentacoes.count(), 2)
        self.assertEqual(movimentacoes[1].tipo_movimento, MovimentacaoEstoque.TipoMovimento.DEVOLUCAO)
        self.assertEqual(movimentacoes[1].quantidade_antes, 6)
        self.assertEqual(movimentacoes[1].quantidade_depois, 8)
        self.assertEqual(entrega.status, EntregaEPI.Status.PARCIALMENTE_DEVOLVIDO)
        self.assertIsNotNone(entrega.data_devolucao)

    def test_nao_permite_entregar_acima_do_saldo_disponivel(self):
        with self.assertRaises(ValidationError):
            EntregaEPI.objects.create(
                funcionario=self.funcionario,
                epi_lote=self.lote,
                quantidade_entregue=11,
                data_entrega=timezone.now(),
                usuario_entrega=self.user,
            )

    def test_nao_permite_reduzir_quantidade_entregue_apos_registro(self):
        entrega = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=4,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )

        entrega.quantidade_entregue = 2

        with self.assertRaises(ValidationError):
            entrega.save()

    def test_status_vira_devolvido_quando_quantidade_devolvida_igual_entregue(self):
        entrega = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=2,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )

        entrega.quantidade_devolvida = 2
        entrega.usuario_devolucao = self.user
        entrega.save()
        entrega.refresh_from_db()

        self.assertEqual(entrega.status, EntregaEPI.Status.DEVOLVIDO)

    def test_nao_permite_devolucao_sem_usuario_devolucao(self):
        entrega = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=2,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )

        entrega.quantidade_devolvida = 1

        with self.assertRaises(ValidationError):
            entrega.save()

    def test_nao_permite_reduzir_quantidade_devolvida_apos_registro(self):
        entrega = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=4,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )
        entrega.quantidade_devolvida = 2
        entrega.usuario_devolucao = self.user
        entrega.save()

        entrega.quantidade_devolvida = 1

        with self.assertRaises(ValidationError):
            entrega.save()

    def test_nao_permite_quantidade_devolvida_maior_que_entregue(self):
        entrega = EntregaEPI(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=2,
            quantidade_devolvida=3,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
            usuario_devolucao=self.user,
        )

        with self.assertRaises(ValidationError):
            entrega.full_clean()

    def test_multiplas_entregas_no_mesmo_lote_consumem_saldo_acumulado(self):
        EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=3,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )
        EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=2,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )

        self.lote.refresh_from_db()
        self.assertEqual(self.lote.quantidade_disponivel, 5)

    def test_devolucao_total_restaura_saldo_do_lote(self):
        entrega = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=4,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )

        entrega.quantidade_devolvida = 4
        entrega.usuario_devolucao = self.user
        entrega.save()

        self.lote.refresh_from_db()
        self.assertEqual(self.lote.quantidade_disponivel, 10)


class MovimentacaoEstoqueModelTests(BaseModelTestCase):
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
