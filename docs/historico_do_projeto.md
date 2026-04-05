# Historico do Projeto

## Etapa 1 - Estrutura Inicial

- projeto base em Django
- configuracao inicial do ambiente com Docker
- PostgreSQL definido como banco de dados do projeto

## Etapa 2 - Ajuste de Infraestrutura do Banco

- separacao confirmada entre aplicacao e banco em containers distintos
- porta externa do PostgreSQL alterada para `55432`
- `healthcheck` adicionado ao servico do banco

## Etapa 3 - Inicio da Modelagem do Banco

- criacao da app de dominio inicial
- implementacao da tabela `setor`
- exposicao de `setor` no admin do Django

## Etapa 4 - Cadastro de Funcionarios

- implementacao da tabela `funcionario`
- relacionamento entre `funcionario` e `setor`
- uso de `PROTECT` para preservar integridade historica
- exposicao de `funcionario` no admin do Django

## Etapa 5 - Cadastro de EPIs

- implementacao da tabela `epi`
- separacao entre cadastro do item e estoque fisico por lote
- indexacao dos campos mais relevantes para busca
- exposicao de `epi` no admin do Django

## Etapa 6 - Controle de Estoque por Lote

- implementacao da tabela `epi_lote`
- relacionamento entre `epi_lote` e `epi`
- constraints de integridade para quantidade e unicidade do lote
- exposicao de `epi_lote` no admin do Django

## Uso Deste Documento
Este arquivo deve ser atualizado a cada etapa relevante para manter o registro da evolucao tecnica e funcional do projeto.
