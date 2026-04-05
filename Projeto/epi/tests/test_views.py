from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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


class AuthViewTests(TestCase):
    def test_login_view_renderiza(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrar")
