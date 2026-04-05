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
Entrada de lote, entrega, devolucao e baixa devem gerar registros em `movimentacao_estoque`, preservando auditoria, historico e rastreabilidade.

### 7. O saldo do lote nao pode ultrapassar a quantidade originalmente recebida
Um lote nao pode registrar `quantidade_disponivel` maior que `quantidade_recebida`.

Essa regra evita um estado invalido de estoque ja na camada de banco e tambem na validacao da aplicacao.

## Regras de Operacao Implementadas

- funcionarios pertencem a um setor
- um EPI pode possuir varios lotes
- entregas apontam para funcionario e lote
- movimentacoes registram alteracoes no estoque
- operacoes criticas de entrega e devolucao usam transacao
- nao e permitido reduzir retroativamente quantidade entregue ou devolvida
- o status da entrega acompanha automaticamente o nivel de devolucao

## Direcao Arquitetural Atual
A aplicacao passou a adotar uma camada de servico para os fluxos de entrega e devolucao.

Essa camada concentra validacoes explicitas de negocio, como:

- funcionario ativo
- lote nao vencido
- saldo suficiente para a entrega
- entrega existente para devolucao
- quantidade devolvida positiva
- devolucao limitada ao saldo pendente da entrega
- baixa limitada ao saldo ainda em aberto da entrega
- baixa com motivo operacional obrigatorio
- baixa nao devolve quantidade ao estoque do lote
- baixa gera movimentacao especifica com motivo associado
- entrada de lote gera movimentacao do tipo `entrada`

Com isso, a regra operacional fica mais visivel fora do model e a arquitetura fica mais preparada para views, formularios e evolucao futura.
