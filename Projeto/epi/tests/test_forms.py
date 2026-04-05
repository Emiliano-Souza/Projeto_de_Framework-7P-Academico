from django.utils import timezone

from epi.forms import DevolucaoEPIForm, EntregaEPIForm
from epi.models import EntregaEPI, Funcionario
from epi.tests.base import BaseModelTestCase


class EntregaEPIFormTests(BaseModelTestCase):
    def test_form_lista_apenas_funcionarios_ativos(self):
        funcionario_inativo = Funcionario.objects.create(
            matricula="F002",
            nome_completo="Carlos Inativo",
            setor=self.setor,
            ativo=False,
        )

        form = EntregaEPIForm()

        self.assertIn(self.funcionario, form.fields["funcionario"].queryset)
        self.assertNotIn(funcionario_inativo, form.fields["funcionario"].queryset)

    def test_form_lista_apenas_lotes_com_saldo_disponivel(self):
        self.lote.quantidade_disponivel = 0
        self.lote.save(update_fields=["quantidade_disponivel"])

        form = EntregaEPIForm()

        self.assertNotIn(self.lote, form.fields["epi_lote"].queryset)

    def test_form_aceita_dados_validos(self):
        form = EntregaEPIForm(
            data={
                "funcionario": self.funcionario.pk,
                "epi_lote": self.lote.pk,
                "quantidade_entregue": 2,
                "data_entrega": "2026-04-05 10:30",
                "confirmado_recebimento": "on",
                "observacao": "Entrega para teste",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_form_configura_campos_para_uso_na_interface(self):
        form = EntregaEPIForm()

        self.assertEqual(form.fields["funcionario"].empty_label, "Selecione um funcionário")
        self.assertEqual(form.fields["epi_lote"].empty_label, "Selecione um lote disponível")
        self.assertEqual(form.fields["data_entrega"].widget.input_type, "datetime-local")
        self.assertIn("form-control", form.fields["observacao"].widget.attrs["class"])


class DevolucaoEPIFormTests(BaseModelTestCase):
    def test_form_lista_apenas_entregas_com_devolucao_pendente(self):
        entrega_pendente = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=3,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )
        entrega_concluida = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=2,
            quantidade_devolvida=2,
            data_entrega=timezone.now(),
            data_devolucao=timezone.now(),
            usuario_entrega=self.user,
            usuario_devolucao=self.user,
        )

        form = DevolucaoEPIForm()

        self.assertIn(entrega_pendente, form.fields["entrega"].queryset)
        self.assertNotIn(entrega_concluida, form.fields["entrega"].queryset)

    def test_form_aceita_dados_validos_para_devolucao(self):
        entrega = EntregaEPI.objects.create(
            funcionario=self.funcionario,
            epi_lote=self.lote,
            quantidade_entregue=3,
            data_entrega=timezone.now(),
            usuario_entrega=self.user,
        )

        form = DevolucaoEPIForm(
            data={
                "entrega": entrega.pk,
                "quantidade_devolvida": 1,
                "observacao": "Retorno parcial para o estoque",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_form_configura_campos_para_uso_na_interface(self):
        form = DevolucaoEPIForm()

        self.assertEqual(form.fields["entrega"].empty_label, "Selecione uma entrega pendente")
        self.assertIn("form-control", form.fields["entrega"].widget.attrs["class"])
        self.assertIn("form-control", form.fields["observacao"].widget.attrs["class"])
