# Regras de Negocio

## Objetivo
Este documento registra as regras funcionais do sistema e deve ser atualizado junto com a evolucao do projeto.

## Regras Ja Consolidadas

### 1. O banco deve usar PostgreSQL
O projeto foi direcionado para PostgreSQL desde a fase inicial de estrutura.

### 2. Os identificadores devem usar BigAutoField
A aplicacao foi configurada para usar identificadores baseados em `BIGINT`, favorecendo consistencia da modelagem desde o inicio.

### 3. Historico nao deve ser tratado com exclusao agressiva
Entidades centrais do dominio devem priorizar protecao referencial e desativacao logica.

### 4. Estoque real nao deve ficar apenas na tabela de EPI
O saldo de estoque precisa ser representado por lotes, evitando inconsistencias entre cadastro do item e controle fisico.

## Regras Previstas Para as Proximas Etapas

- funcionarios pertencem a um setor
- um EPI pode possuir varios lotes
- entregas devem apontar para funcionario e lote
- movimentacoes devem registrar alteracoes no estoque
- operacoes criticas devem ser feitas em transacao
