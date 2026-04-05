from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from epi.models import EntregaEPI, MovimentacaoEstoque
from epi.services.entregas import registrar_entrega_epi
from epi.tests.base import BaseModelTestCase


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


class EntregaEPIServiceTests(BaseModelTestCase):
    def test_service_bloqueia_funcionario_inativo(self):
        self.funcionario.ativo = False
        self.funcionario.save(update_fields=["ativo"])

        with self.assertRaises(ValidationError):
            registrar_entrega_epi(
                funcionario=self.funcionario,
                epi_lote=self.lote,
                quantidade_entregue=1,
                usuario_entrega=self.user,
            )

    def test_service_bloqueia_lote_vencido(self):
        self.lote.data_validade = timezone.now().date() - timedelta(days=1)
        self.lote.save(update_fields=["data_validade"])

        with self.assertRaises(ValidationError):
            registrar_entrega_epi(
                funcionario=self.funcionario,
                epi_lote=self.lote,
                quantidade_entregue=1,
                usuario_entrega=self.user,
            )

    def test_service_registra_entrega_com_sucesso(self):
        entrega = registrar_entrega_epi(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=2,
            usuario_entrega=self.user,
            confirmado_recebimento=True,
            observacao="Entrega via service",
        )

        self.lote.refresh_from_db()

        self.assertEqual(self.lote.quantidade_disponivel, 8)
        self.assertEqual(entrega.quantidade_entregue, 2)
        self.assertTrue(entrega.confirmado_recebimento)
