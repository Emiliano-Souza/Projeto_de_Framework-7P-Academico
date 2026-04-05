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

## Proximas Etapas Planejadas
As proximas tabelas previstas sao:

1. `funcionario`
2. `epi`
3. `epi_lote`
4. `entrega_epi`
5. `movimentacao_estoque`

## Principios de Modelagem
Os principios adotados para a modelagem sao:

- evitar `CASCADE` em entidades com historico
- preferir desativacao logica em vez de exclusao fisica
- separar cadastro de item e saldo de estoque
- rastrear movimentacoes de estoque
- aplicar constraints e indices onde fizer sentido
