from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from epi.models import EPI, EPILote, EntregaEPI, Funcionario, MovimentacaoEstoque, Setor
from epi.services.entregas import registrar_entrega_epi
from epi.tests.base import BaseModelTestCase


class PermissaoViewTests(TestCase):
    def setUp(self):
        self.user_sem_grupo = get_user_model().objects.create_user(
            username="sem_grupo", password="123"
        )
        self.user_gestor = get_user_model().objects.create_user(
            username="gestor", password="123"
        )
        grupo_gestor, _ = Group.objects.get_or_create(name="Gestor")
        self.user_gestor.groups.add(grupo_gestor)

        self.user_almoxarife = get_user_model().objects.create_user(
            username="almoxarife", password="123"
        )
        grupo_alm, _ = Group.objects.get_or_create(name="Almoxarife")
        self.user_almoxarife.groups.add(grupo_alm)

    def test_usuario_sem_grupo_nao_acessa_entrega(self):
        self.client.force_login(self.user_sem_grupo)
        response = self.client.get(reverse("epi:registrar_entrega"))
        self.assertEqual(response.status_code, 403)

    def test_gestor_nao_acessa_entrega(self):
        self.client.force_login(self.user_gestor)
        response = self.client.get(reverse("epi:registrar_entrega"))
        self.assertEqual(response.status_code, 403)

    def test_gestor_nao_acessa_devolucao(self):
        self.client.force_login(self.user_gestor)
        response = self.client.get(reverse("epi:registrar_devolucao"))
        self.assertEqual(response.status_code, 403)

    def test_gestor_nao_acessa_baixa(self):
        self.client.force_login(self.user_gestor)
        response = self.client.get(reverse("epi:registrar_baixa"))
        self.assertEqual(response.status_code, 403)

    def test_almoxarife_acessa_entrega(self):
        self.client.force_login(self.user_almoxarife)
        response = self.client.get(reverse("epi:registrar_entrega"))
        self.assertEqual(response.status_code, 200)

    def test_almoxarife_acessa_devolucao(self):
        self.client.force_login(self.user_almoxarife)
        response = self.client.get(reverse("epi:registrar_devolucao"))
        self.assertEqual(response.status_code, 200)

    def test_almoxarife_acessa_baixa(self):
        self.client.force_login(self.user_almoxarife)
        response = self.client.get(reverse("epi:registrar_baixa"))
        self.assertEqual(response.status_code, 200)

    def test_usuario_nao_autenticado_e_redirecionado_para_login(self):
        response = self.client.get(reverse("epi:registrar_entrega"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_gestor_acessa_dashboard(self):
        self.client.force_login(self.user_gestor)
        response = self.client.get(reverse("epi:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_gestor_acessa_movimentacoes(self):
        self.client.force_login(self.user_gestor)
        response = self.client.get(reverse("epi:listar_movimentacoes"))
        self.assertEqual(response.status_code, 200)


class TransacaoComErroTests(BaseModelTestCase):
    def test_entrega_com_saldo_insuficiente_nao_altera_lote(self):
        saldo_antes = self.lote.quantidade_disponivel

        with self.assertRaises(ValidationError):
            registrar_entrega_epi(
                funcionario=self.funcionario,
                epi_lote=self.lote,
                quantidade_entregue=999,
                usuario_entrega=self.user,
            )

        self.lote.refresh_from_db()
        self.assertEqual(self.lote.quantidade_disponivel, saldo_antes)

    def test_entrega_com_erro_nao_cria_movimentacao(self):
        total_antes = MovimentacaoEstoque.objects.count()

        with self.assertRaises(ValidationError):
            registrar_entrega_epi(
                funcionario=self.funcionario,
                epi_lote=self.lote,
                quantidade_entregue=999,
                usuario_entrega=self.user,
            )

        self.assertEqual(MovimentacaoEstoque.objects.count(), total_antes)

    def test_entrega_com_erro_nao_cria_registro_de_entrega(self):
        total_antes = EntregaEPI.objects.count()

        with self.assertRaises(ValidationError):
            registrar_entrega_epi(
                funcionario=self.funcionario,
                epi_lote=self.lote,
                quantidade_entregue=999,
                usuario_entrega=self.user,
            )

        self.assertEqual(EntregaEPI.objects.count(), total_antes)

    def test_erro_no_save_do_lote_faz_rollback_completo(self):
        saldo_antes = self.lote.quantidade_disponivel
        total_entregas_antes = EntregaEPI.objects.count()
        total_mov_antes = MovimentacaoEstoque.objects.count()

        with patch(
            "epi.models.EPILote.save",
            side_effect=Exception("Erro simulado no banco"),
        ):
            with self.assertRaises(Exception):
                registrar_entrega_epi(
                    funcionario=self.funcionario,
                    epi_lote=self.lote,
                    quantidade_entregue=1,
                    usuario_entrega=self.user,
                )

        self.lote.refresh_from_db()
        self.assertEqual(self.lote.quantidade_disponivel, saldo_antes)
        self.assertEqual(EntregaEPI.objects.count(), total_entregas_antes)
        self.assertEqual(MovimentacaoEstoque.objects.count(), total_mov_antes)
