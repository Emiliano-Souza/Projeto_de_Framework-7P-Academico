# Decisoes Tecnicas

## 1. Separacao entre banco e aplicacao
Decisao:
Executar PostgreSQL e Django em containers separados.

Motivo:
Essa abordagem melhora organizacao da infraestrutura, facilita manutencao e reduz conflitos de responsabilidade.

## 2. Porta externa do PostgreSQL fora do padrao
Decisao:
Publicar o PostgreSQL na porta `55432` no host local.

Motivo:
Reduz o risco de conflito com outra instalacao local de PostgreSQL usando a porta `5432`.

## 3. Uso de healthcheck no servico do banco
Decisao:
Adicionar `healthcheck` com `pg_isready` no servico `db`.

Motivo:
Permite verificar se o PostgreSQL esta realmente pronto para aceitar conexoes.

## 4. Criacao de uma app de dominio para o sistema
Decisao:
Centralizar a modelagem inicial do dominio em uma app Django dedicada.

Motivo:
Melhora a organizacao do projeto e agrupa modelos, admin e migracoes em um unico modulo funcional.

## 5. Construir primeiro a camada de banco
Decisao:
Evoluir o sistema em etapas, com foco inicial na modelagem do banco antes das telas.

Motivo:
Isso reduz retrabalho, torna a regra de negocio mais clara e facilita documentacao tecnica consistente.

## 6. Migrar gradualmente a regra operacional para services
Decisao:
Mover a orquestracao de entrega, devolucao e baixa para camada de service, mantendo compatibilidade com o model.

Motivo:

- deixa a regra mais explicita
- melhora testabilidade
- evita acoplamento excessivo nas views
- preserva consistencia no admin e no ORM

## 7. Manter `EntregaEPI` como entidade operacional central
Decisao:
Usar `EntregaEPI` como ponto central para entrega, devolucao e baixa.

Motivo:

- simplifica a rastreabilidade
- facilita o uso de deltas
- evita criar tabelas de operacao separadas cedo demais

## 8. Usar `MovimentacaoEstoque` como trilha unica de auditoria
Decisao:
Toda operacao relevante de estoque deve gerar uma linha em `movimentacao_estoque`.

Motivo:

- melhora auditoria
- centraliza historico
- facilita tela de rastreabilidade
- fortalece o projeto academicamente

## 9. Separar views e URLs por fluxo funcional
Decisao:
Organizar a camada web em modulos como `views/entregas.py`, `views/devolucoes.py`, `views/baixas.py` e equivalentes em `urls/`.

Motivo:

- evita arquivos monoliticos
- deixa a navegacao no codigo mais clara
- prepara o projeto para crescer sem bagunca

## 10. Usar filtros de queryset nos formularios
Decisao:
Deixar os formularios mostrarem apenas opcoes operacionais validas.

Motivo:

- melhora a UX
- reduz erro humano
- complementa, sem substituir, a validacao do service

## 11. Tratar baixa sem alterar saldo do lote
Decisao:
Registrar baixa como encerramento de quantidade entregue sem retorno fisico ao estoque.

Motivo:

- o lote ja foi reduzido no momento da entrega
- a baixa eh um evento operacional, nao uma devolucao
- isso preserva o sentido correto do saldo do lote

## 12. Manter documentacao tecnica junto da evolucao do codigo
Decisao:
Atualizar a documentacao a cada etapa importante do projeto.

Motivo:

- evita documentacao desatualizada
- ajuda onboarding tecnico
- melhora apresentacao e manutencao
