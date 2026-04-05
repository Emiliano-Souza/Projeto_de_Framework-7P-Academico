from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from epi.models import EntregaEPI, Setor
from epi.tests.base import BaseModelTestCase


class RegistrarEntregaViewTests(BaseModelTestCase):
    def test_view_exige_autenticacao(self):
        response = self.client.get(reverse("epi:registrar_entrega"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_renderiza_formulario_para_usuario_logado(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("epi:registrar_entrega"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Registrar Entrega de EPI")
        self.assertContains(response, "Antes de salvar")
        self.assertContains(response, "Voltar ao painel administrativo")

    def test_view_registra_entrega_com_sucesso(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("epi:registrar_entrega"),
            data={
                "funcionario": self.funcionario.pk,
                "epi_lote": self.lote.pk,
                "quantidade_entregue": 2,
                "data_entrega": "2026-04-05 10:30",
                "confirmado_recebimento": "on",
                "observacao": "Entrega via view",
            },
            follow=True,
        )

        self.lote.refresh_from_db()
        entrega = EntregaEPI.objects.get()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrega registrada com sucesso.")
        self.assertEqual(self.lote.quantidade_disponivel, 8)
        self.assertEqual(entrega.usuario_entrega, self.user)

    def test_view_mostra_erro_para_funcionario_inativo(self):
        self.client.force_login(self.user)
        self.funcionario.ativo = False
        self.funcionario.save(update_fields=["ativo"])

        response = self.client.post(
            reverse("epi:registrar_entrega"),
            data={
                "funcionario": self.funcionario.pk,
                "epi_lote": self.lote.pk,
                "quantidade_entregue": 1,
                "data_entrega": "2026-04-05 10:30",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice.")


class RegistrarDevolucaoViewTests(BaseModelTestCase):
    def setUp(self):
        super().setUp()
        self.entrega = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=4,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )

    def test_view_exige_autenticacao(self):
        response = self.client.get(reverse("epi:registrar_devolucao"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_renderiza_formulario_para_usuario_logado(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("epi:registrar_devolucao"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Registrar Devolucao de EPI")
        self.assertContains(response, "Dados da devolução")
        self.assertContains(response, "Voltar para entregas")

    def test_view_registra_devolucao_com_sucesso(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("epi:registrar_devolucao"),
            data={
                "entrega": self.entrega.pk,
                "quantidade_devolvida": 2,
                "observacao": "Devolucao via view",
            },
            follow=True,
        )

        self.entrega.refresh_from_db()
        self.lote.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Devolucao registrada com sucesso.")
        self.assertEqual(self.entrega.quantidade_devolvida, 2)
        self.assertEqual(self.lote.quantidade_disponivel, 8)
        self.assertEqual(self.entrega.usuario_devolucao, self.user)

    def test_view_mostra_erro_para_devolucao_maior_que_saldo_pendente(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("epi:registrar_devolucao"),
            data={
                "entrega": self.entrega.pk,
                "quantidade_devolvida": 5,
                "observacao": "Tentativa invalida",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "A quantidade devolvida nao pode ser maior que o saldo pendente da entrega.",
        )


class AuthViewTests(TestCase):
    def test_login_view_renderiza(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrar")
