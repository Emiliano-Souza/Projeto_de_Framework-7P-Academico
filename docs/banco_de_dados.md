# Banco de Dados

## Tecnologia
O projeto utiliza PostgreSQL como banco de dados relacional principal.

No Django, o identificador padrao esta configurado como `BigAutoField`, o que alinha o projeto ao uso de chaves primarias baseadas em `BIGINT`.

## Direcao da Modelagem
A modelagem planejada para o sistema considera as seguintes tabelas principais:

- `setor`
- `funcionario`
- `epi`
- `epi_lote`
- `entrega_epi`
- `movimentacao_estoque`

Tambem sao aproveitadas as tabelas nativas do Django:

- `auth_user`
- `auth_group`
- `auth_permission`

## Primeira Etapa Implementada
A primeira tabela implementada foi `setor`.

### Tabela `setor`
Finalidade:
Padronizar os setores da empresa e evitar registros textuais inconsistentes no cadastro de funcionarios.

Campos atuais:

- `id`
- `nome`
- `descricao`
- `ativo`
- `created_at`
- `updated_at`

Decisoes aplicadas:

- `id` com `BigAutoField`
- `nome` obrigatorio e unico
- `ativo` para desativacao logica
- timestamps de criacao e atualizacao
- nome fisico da tabela definido como `setor`

## Segunda Etapa Implementada
A segunda tabela implementada foi `funcionario`.

### Tabela `funcionario`
Finalidade:
Representar a pessoa que recebera EPIs dentro do contexto da empresa.

Campos atuais:

- `id`
- `matricula`
- `nome_completo`
- `setor_id`
- `cargo`
- `data_admissao`
- `ativo`
- `observacao`
- `created_at`
- `updated_at`

Decisoes aplicadas:

- `id` com `BigAutoField`
- `matricula` obrigatoria e unica
- `nome_completo` indexado para busca
- relacionamento com `setor` usando `PROTECT`
- `ativo` para desativacao logica
- timestamps de criacao e atualizacao
- nome fisico da tabela definido como `funcionario`

## Terceira Etapa Implementada
A terceira tabela implementada foi `epi`.

### Tabela `epi`
Finalidade:
Representar o cadastro do item de EPI, sem concentrar o saldo fisico real do estoque.

Campos atuais:

- `id`
- `codigo_interno`
- `nome`
- `descricao`
- `categoria`
- `fabricante`
- `numero_ca`
- `controla_tamanho`
- `estoque_minimo`
- `ativo`
- `created_at`
- `updated_at`

Decisoes aplicadas:

- `id` com `BigAutoField`
- `codigo_interno` obrigatorio e unico
- `nome` indexado para busca
- `numero_ca` indexado
- `estoque_minimo` como parametro de alerta, nao como saldo real
- `ativo` para desativacao logica
- timestamps de criacao e atualizacao
- nome fisico da tabela definido como `epi`

## Quarta Etapa Implementada
A quarta tabela implementada foi `epi_lote`.

### Tabela `epi_lote`
Finalidade:
Representar o estoque fisico por lote, com validade, saldo disponivel e dados de entrada.

Campos atuais:

- `id`
- `epi_id`
- `numero_lote`
- `data_fabricacao`
- `data_validade`
- `quantidade_recebida`
- `quantidade_disponivel`
- `local_armazenamento`
- `valor_unitario`
- `created_at`
- `updated_at`

Decisoes aplicadas:

- `id` com `BigAutoField`
- relacionamento com `epi` usando `PROTECT`
- `data_validade` indexada
- unicidade por `epi` e `numero_lote`
- constraint para garantir `quantidade_recebida > 0`
- constraint para garantir `quantidade_disponivel >= 0`
- constraint para garantir `quantidade_disponivel <= quantidade_recebida`
- nome fisico da tabela definido como `epi_lote`

## Quinta Etapa Implementada
A quinta tabela implementada foi `entrega_epi`.

### Tabela `entrega_epi`
Finalidade:
Registrar a operacao de entrega de um lote de EPI para um funcionario, com controle de devolucao e status.

Campos atuais:

- `id`
- `funcionario_id`
- `epi_lote_id`
- `quantidade_entregue`
- `quantidade_devolvida`
- `quantidade_baixada`
- `data_entrega`
- `data_devolucao`
- `status`
- `confirmado_recebimento`
- `usuario_entrega_id`
- `usuario_devolucao_id`
- `usuario_baixa_id`
- `observacao`
- `created_at`
- `updated_at`

Decisoes aplicadas:

- `id` com `BigAutoField`
- relacionamento com `funcionario` usando `PROTECT`
- relacionamento com `epi_lote` usando `PROTECT`
- uso de `auth_user` do Django para registrar usuarios da operacao
- `usuario_baixa` separado de `usuario_devolucao` para preservar historico correto
- `data_entrega` indexada
- `status` implementado com `choices`
- constraint para garantir `quantidade_entregue > 0`
- constraint para garantir `quantidade_devolvida >= 0`
- constraint para garantir `quantidade_devolvida <= quantidade_entregue`
- constraint para garantir `quantidade_devolvida + quantidade_baixada <= quantidade_entregue`
- nome fisico da tabela definido como `entrega_epi`

## Sexta Etapa Implementada
A sexta tabela implementada foi `movimentacao_estoque`.

### Tabela `movimentacao_estoque`
Finalidade:
Registrar cada alteracao relevante no estoque para fins de auditoria, historico e rastreabilidade.

Campos atuais:

- `id`
- `epi_lote_id`
- `tipo_movimento`
- `quantidade`
- `quantidade_antes`
- `quantidade_depois`
- `funcionario_id`
- `entrega_epi_id`
- `usuario_id`
- `motivo`
- `observacao`
- `created_at`

Decisoes aplicadas:

- `id` com `BigAutoField`
- relacionamento com `epi_lote` usando `PROTECT`
- relacionamento opcional com `funcionario`
- relacionamento opcional com `entrega_epi`
- uso de `auth_user` do Django para auditoria do responsavel
- `created_at` indexado
- `tipo_movimento` implementado com `choices`
- tipo `baixa` reservado para o fluxo de encerramento sem retorno ao estoque
- constraint para garantir `quantidade > 0`
- constraint para garantir `quantidade_antes >= 0`
- constraint para garantir `quantidade_depois >= 0`
- validacao explicita via `clean()` no model para `quantidade > 0` e `quantidade_depois >= 0`
- nome fisico da tabela definido como `movimentacao_estoque`

## Proximas Etapas Planejadas
As tabelas principais previstas para a modelagem inicial foram concluidas.

## Refinamentos Aplicados

- validacao para impedir lote com saldo maior que a quantidade recebida
- ajuste automatico do status de `entrega_epi` conforme o nivel de devolucao
- service de entrada de lote com geracao de `movimentacao_estoque` do tipo `entrada`

## Principios de Modelagem
Os principios adotados para a modelagem sao:

- evitar `CASCADE` em entidades com historico
- preferir desativacao logica em vez de exclusao fisica
- separar cadastro de item e saldo de estoque
- rastrear movimentacoes de estoque
- aplicar constraints e indices onde fizer sentido
