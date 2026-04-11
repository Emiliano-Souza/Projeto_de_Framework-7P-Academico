# Arquitetura do Projeto

## Objetivo
O sistema foi concebido para gerenciar a entrega de Equipamentos de Protecao Individual (EPIs), com foco em cadastro, estoque, validade, historico de entrega e rastreabilidade.

## Visao Geral
O projeto utiliza Django como framework principal e PostgreSQL como banco de dados relacional. A aplicacao e o banco sao executados em containers separados, orquestrados por Docker Compose.

No estado atual, a aplicacao ja possui:

- modelagem principal do dominio implementada
- camada de service para operacoes de estoque
- autenticacao basica com Django auth
- fluxos web de entrega, devolucao e baixa
- tela de historico de movimentacoes
- suite de testes automatizados

## Estrutura Atual
Atualmente o projeto possui dois servicos principais:

- `db`: container responsavel pelo PostgreSQL
- `django`: container responsavel pela aplicacao Django

Essa separacao melhora a organizacao da infraestrutura, facilita manutencao e reduz acoplamento entre aplicacao e banco.

## Fluxo de Inicializacao
O fluxo atual de subida do ambiente e o seguinte:

1. O Docker Compose inicia o container do PostgreSQL.
2. O Docker Compose aguarda o healthcheck do banco passar (`pg_isready`).
3. O Docker Compose inicia o container do Django.
4. O `entrypoint.sh` do Django aguarda o banco aceitar conexao.
5. O Django executa as migracoes pendentes.
6. O servidor de desenvolvimento e iniciado na porta `8000`.

## Comunicacao Entre Servicos
Dentro da rede do Docker Compose:

- o Django acessa o banco pelo host `db`
- a porta interna do PostgreSQL permanece `5432`

Fora do Docker, a porta publicada do banco foi alterada para `55432`, reduzindo risco de conflito com outras instalacoes locais do PostgreSQL.

## Organizacao do Codigo
A organizacao atual do codigo e composta por:

- `Projeto/config`: configuracoes principais do Django
- `Projeto/epi`: app de dominio do sistema
- `Projeto/docker-compose.yml`: definicao dos servicos do ambiente
- `Projeto/entrypoint.sh`: script de inicializacao da aplicacao

Dentro da app `epi`, a organizacao principal esta distribuida em:

- `models.py`: entidades e integridade estrutural
- `forms.py`: formularios operacionais
- `services/`: regra de negocio e orquestracao
- `views/`: camada HTTP
- `urls/`: agrupamento de rotas por fluxo
- `templates/epi/`: telas HTML dos fluxos
- `tests/`: cobertura automatizada por responsabilidade

## Componentes Funcionais Atuais

Os principais componentes funcionais implementados hoje sao:

- entrada de lote com rastreabilidade
- entrega de EPI
- devolucao de EPI
- baixa de EPI
- historico de movimentacoes de estoque

Esses fluxos compartilham a mesma base tecnica:

- `EntregaEPI` como entidade operacional central
- `MovimentacaoEstoque` como trilha de auditoria
- camada de service para coordenar persistencia e regras

## Direcao Arquitetural
O projeto foi construido por etapas: primeiro banco e dominio, depois regras operacionais, e por fim fluxos web.

A direcao atual prioriza:

- consolidar a rastreabilidade do estoque
- manter a regra critica fora das views
- usar o Django de forma organizada por camadas
- documentar e testar cada evolucao relevante
