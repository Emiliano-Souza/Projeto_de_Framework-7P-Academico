from epi.forms import EntregaEPIForm
from epi.models import Funcionario
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
