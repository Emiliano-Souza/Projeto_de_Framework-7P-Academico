# Arquitetura do Projeto

## Objetivo
O sistema foi concebido para gerenciar a entrega de Equipamentos de Protecao Individual (EPIs), com foco em cadastro, estoque, validade, historico de entrega e rastreabilidade.

## Visao Geral
O projeto utiliza Django como framework principal e PostgreSQL como banco de dados relacional. A aplicacao e o banco sao executados em containers separados, orquestrados por Docker Compose.

## Estrutura Atual
Atualmente o projeto possui dois servicos principais:

- `db`: container responsavel pelo PostgreSQL
- `django`: container responsavel pela aplicacao Django

Essa separacao melhora a organizacao da infraestrutura, facilita manutencao e reduz acoplamento entre aplicacao e banco.

## Fluxo de Inicializacao
O fluxo atual de subida do ambiente e o seguinte:

1. O Docker Compose inicia o container do PostgreSQL.
2. O Docker Compose inicia o container do Django.
3. O `entrypoint.sh` do Django aguarda o banco aceitar conexao.
4. O Django executa as migracoes pendentes.
5. O servidor de desenvolvimento e iniciado na porta `8000`.

## Comunicacao Entre Servicos
Dentro da rede do Docker Compose:

- o Django acessa o banco pelo host `db`
- a porta interna do PostgreSQL permanece `5432`

Fora do Docker, a porta publicada do banco foi alterada para `55432`, reduzindo risco de conflito com outras instalacoes locais do PostgreSQL.

## Organizacao do Codigo
A organizacao atual do codigo e composta por:

- `Projeto/config`: configuracoes principais do Django
- `Projeto/epi`: app de dominio inicial do sistema
- `Projeto/docker-compose.yml`: definicao dos servicos do ambiente
- `Projeto/entrypoint.sh`: script de inicializacao da aplicacao

## Direcao Arquitetural
O projeto esta sendo construido por etapas. A intencao e consolidar primeiro a camada de banco de dados e a estrutura do dominio, e depois evoluir para regras operacionais, telas e fluxos de uso.
