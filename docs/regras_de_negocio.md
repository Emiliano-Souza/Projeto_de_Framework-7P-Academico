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

### 5. Operacoes de entrega e devolucao devem preservar consistencia do lote
Ao registrar uma entrega, o sistema deve baixar a quantidade disponivel do lote.

Ao registrar uma devolucao, o sistema deve devolver saldo ao lote.

Essas operacoes precisam ocorrer dentro de transacao para evitar inconsistencias entre entrega registrada e saldo fisico.

### 6. Toda alteracao operacional relevante deve gerar movimentacao de estoque
Entrega e devolucao devem gerar registros em `movimentacao_estoque`, preservando auditoria, historico e rastreabilidade.

## Regras de Operacao Implementadas

- funcionarios pertencem a um setor
- um EPI pode possuir varios lotes
- entregas apontam para funcionario e lote
- movimentacoes registram alteracoes no estoque
- operacoes criticas de entrega e devolucao usam transacao
- nao e permitido reduzir retroativamente quantidade entregue ou devolvida
