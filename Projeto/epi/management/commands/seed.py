from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from epi.models import EPI, EPILote, Funcionario, Setor
from epi.services.entregas import registrar_baixa_epi, registrar_devolucao_epi, registrar_entrega_epi
from epi.services.lotes import registrar_entrada_lote

User = get_user_model()


class Command(BaseCommand):
    help = "Popula o banco com dados de demonstracao"

    def handle(self, *args, **kwargs):
        self.stdout.write("Criando dados de demonstracao...")

        user = self._criar_usuario()
        setores = self._criar_setores()
        funcionarios = self._criar_funcionarios(setores)
        epis = self._criar_epis()
        lotes = self._criar_lotes(epis, user)
        self._criar_entregas_e_operacoes(funcionarios, lotes, user)

        self.stdout.write(self.style.SUCCESS("Dados criados com sucesso."))

    def _criar_usuario(self):
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={"is_staff": True, "is_superuser": True},
        )
        if created:
            user.set_password("admin")
            user.save()
            self.stdout.write("  Usuario admin criado (senha: admin)")

        # almoxarife
        almoxarife, created = User.objects.get_or_create(
            username="almoxarife",
            defaults={"is_staff": False, "is_superuser": False},
        )
        if created:
            almoxarife.set_password("almoxarife")
            almoxarife.save()
        from django.contrib.auth.models import Group
        grupo_alm, _ = Group.objects.get_or_create(name="Almoxarife")
        almoxarife.groups.set([grupo_alm])
        self.stdout.write("  Usuario almoxarife criado (senha: almoxarife)")

        # gestor
        gestor, created = User.objects.get_or_create(
            username="gestor",
            defaults={"is_staff": False, "is_superuser": False},
        )
        if created:
            gestor.set_password("gestor")
            gestor.save()
        grupo_ges, _ = Group.objects.get_or_create(name="Gestor")
        gestor.groups.set([grupo_ges])
        self.stdout.write("  Usuario gestor criado (senha: gestor)")

        return user

    def _criar_setores(self):
        dados = [
            ("Producao", "Linha de producao e montagem"),
            ("Manutencao", "Manutencao preventiva e corretiva"),
            ("Logistica", "Armazem e movimentacao de cargas"),
            ("Qualidade", "Controle e inspecao de qualidade"),
            ("Administrativo", "Escritorio e suporte administrativo"),
        ]
        setores = []
        for nome, descricao in dados:
            s, _ = Setor.objects.get_or_create(nome=nome, defaults={"descricao": descricao})
            setores.append(s)
        self.stdout.write(f"  {len(setores)} setores criados")
        return setores

    def _criar_funcionarios(self, setores):
        dados = [
            ("F001", "Ana Paula Souza", setores[0], "Operadora"),
            ("F002", "Carlos Eduardo Lima", setores[0], "Operador"),
            ("F003", "Fernanda Costa", setores[0], "Supervisora"),
            ("F004", "Roberto Alves", setores[1], "Tecnico"),
            ("F005", "Juliana Martins", setores[1], "Tecnica"),
            ("F006", "Marcos Pereira", setores[2], "Auxiliar de Logistica"),
            ("F007", "Patricia Oliveira", setores[2], "Conferente"),
            ("F008", "Diego Santos", setores[3], "Inspetor"),
            ("F009", "Camila Ferreira", setores[3], "Analista"),
            ("F010", "Lucas Rodrigues", setores[4], "Assistente"),
            ("F011", "Beatriz Nascimento", setores[0], "Operadora"),
            ("F012", "Thiago Carvalho", setores[1], "Eletricista"),
            ("F013", "Renata Gomes", setores[2], "Motorista"),
            ("F014", "Anderson Silva", setores[0], "Operador", False),
            ("F015", "Vanessa Mendes", setores[3], "Inspetora", False),
        ]
        funcionarios = []
        for item in dados:
            matricula, nome, setor, cargo = item[0], item[1], item[2], item[3]
            ativo = item[4] if len(item) > 4 else True
            f, _ = Funcionario.objects.get_or_create(
                matricula=matricula,
                defaults={
                    "nome_completo": nome,
                    "setor": setor,
                    "cargo": cargo,
                    "ativo": ativo,
                    "data_admissao": date(2022, 1, 10),
                },
            )
            if ativo:
                funcionarios.append(f)
        self.stdout.write(f"  15 funcionarios criados (13 ativos, 2 inativos)")
        return funcionarios

    def _criar_epis(self):
        dados = [
            ("EPI-001", "Capacete de Seguranca", "Protecao da Cabeca", "3M", "CA-12345", 10),
            ("EPI-002", "Luva de Vaqueta", "Protecao das Maos", "Kalipso", "CA-23456", 20),
            ("EPI-003", "Botina de Seguranca", "Protecao dos Pes", "Marluvas", "CA-34567", 5),
            ("EPI-004", "Oculos de Protecao", "Protecao Visual", "3M", "CA-45678", 15),
            ("EPI-005", "Protetor Auricular", "Protecao Auditiva", "Moldex", "CA-56789", 30),
            ("EPI-006", "Colete Refletivo", "Sinalizacao", "Delta Plus", "CA-67890", 8),
            ("EPI-007", "Mascara PFF2", "Protecao Respiratoria", "3M", "CA-78901", 50),
            ("EPI-008", "Cinto de Seguranca", "Trabalho em Altura", "Petzl", "CA-89012", 3),
        ]
        epis = []
        for codigo, nome, categoria, fabricante, ca, minimo in dados:
            e, _ = EPI.objects.get_or_create(
                codigo_interno=codigo,
                defaults={
                    "nome": nome,
                    "categoria": categoria,
                    "fabricante": fabricante,
                    "numero_ca": ca,
                    "estoque_minimo": minimo,
                },
            )
            epis.append(e)
        self.stdout.write(f"  {len(epis)} EPIs criados")
        return epis

    def _criar_lotes(self, epis, user):
        hoje = date.today()
        dados = [
            (epis[0], "L2024-001", 50, hoje + timedelta(days=365)),
            (epis[0], "L2023-001", 20, hoje - timedelta(days=30)),   # vencido
            (epis[1], "L2024-002", 100, hoje + timedelta(days=180)),
            (epis[1], "L2024-003", 30, hoje + timedelta(days=20)),   # proximo do vencimento
            (epis[2], "L2024-004", 40, hoje + timedelta(days=730)),
            (epis[3], "L2024-005", 60, hoje + timedelta(days=500)),
            (epis[4], "L2024-006", 200, hoje + timedelta(days=300)),
            (epis[5], "L2024-007", 25, hoje + timedelta(days=400)),
            (epis[6], "L2024-008", 150, hoje + timedelta(days=180)),
            (epis[7], "L2024-009", 10, hoje + timedelta(days=1000)),
        ]
        lotes = []
        for epi, numero, qtd, validade in dados:
            if not EPILote.objects.filter(epi=epi, numero_lote=numero).exists():
                lote = registrar_entrada_lote(
                    epi=epi,
                    numero_lote=numero,
                    quantidade_recebida=qtd,
                    usuario_responsavel=user,
                    data_validade=validade,
                    observacao="Entrada via seed de demonstracao",
                )
                lotes.append(lote)
            else:
                lotes.append(EPILote.objects.get(epi=epi, numero_lote=numero))
        self.stdout.write(f"  {len(lotes)} lotes criados (1 vencido, 1 proximo do vencimento)")
        return lotes

    def _criar_entregas_e_operacoes(self, funcionarios, lotes, user):
        now = timezone.now()

        operacoes = [
            (funcionarios[0], lotes[0], 2),
            (funcionarios[1], lotes[0], 1),
            (funcionarios[2], lotes[2], 3),
            (funcionarios[3], lotes[4], 1),
            (funcionarios[4], lotes[5], 2),
            (funcionarios[5], lotes[6], 5),
            (funcionarios[6], lotes[7], 1),
            (funcionarios[7], lotes[3], 2),
            (funcionarios[8], lotes[8], 4),
            (funcionarios[9], lotes[9], 1),
        ]

        entregas = []
        for funcionario, lote, qtd in operacoes:
            if lote.quantidade_disponivel >= qtd:
                e = registrar_entrega_epi(
                    funcionario=funcionario,
                    epi_lote=lote,
                    quantidade_entregue=qtd,
                    usuario_entrega=user,
                    confirmado_recebimento=True,
                    observacao="Entrega via seed de demonstracao",
                )
                entregas.append(e)

        # devolucao parcial na primeira entrega
        if entregas:
            registrar_devolucao_epi(
                entrega_id=entregas[0].pk,
                quantidade_devolvida=1,
                usuario_devolucao=user,
                observacao="Devolucao via seed de demonstracao",
            )

        # baixa na segunda entrega
        if len(entregas) > 1:
            registrar_baixa_epi(
                entrega_id=entregas[1].pk,
                quantidade_baixada=1,
                usuario_baixa=user,
                motivo_baixa="danificado",
                observacao="Item danificado em uso",
            )

        self.stdout.write(f"  {len(entregas)} entregas criadas (1 devolucao, 1 baixa)")
