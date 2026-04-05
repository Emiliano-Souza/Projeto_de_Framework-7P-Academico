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

## Etapa 7 - Registro de Entregas de EPI

- implementacao da tabela `entrega_epi`
- relacionamento entre entrega, funcionario, lote e usuario do sistema
- definicao de status para acompanhar o ciclo da entrega
- constraints para garantir coerencia entre quantidade entregue e devolvida
- exposicao de `entrega_epi` no admin do Django

## Etapa 8 - Auditoria de Estoque

- implementacao da tabela `movimentacao_estoque`
- registro do tipo de movimento, saldo anterior e saldo posterior
- relacionamento com lote, entrega, funcionario e usuario do sistema
- constraints basicas para integridade dos registros
- exposicao de `movimentacao_estoque` no admin do Django

## Etapa 9 - Regra Operacional de Entrega e Devolucao

- integracao entre `entrega_epi`, `epi_lote` e `movimentacao_estoque`
- baixa automatica do lote ao registrar entrega
- retorno automatica de saldo ao registrar devolucao
- uso de transacao para preservar consistencia

## Etapa 10 - Refinos de Integridade

- regra para impedir saldo de lote acima da quantidade recebida
- ajuste automatico do status da entrega com base na devolucao

## Etapa 11 - Testes Automatizados Iniciais

- criacao de testes para integridade de `epi_lote`
- criacao de testes para fluxo de entrega e devolucao
- verificacao automatizada de baixa de saldo e geracao de movimentacao

## Etapa 12 - Expansao dos Testes de Borda

- testes para unicidade de lote por EPI
- testes para devolucao invalida
- testes para consumo acumulado do mesmo lote
- testes para restauracao total de saldo

## Etapa 13 - Testes de Integridade Estrutural

- testes para unicidade de setor, funcionario e EPI
- testes para comportamento de `PROTECT`
- testes para validacao basica de `movimentacao_estoque`

## Etapa 14 - Organizacao da Suite de Testes

- separacao dos testes por responsabilidade
- criacao de pasta `tests/` para o dominio `epi`
- reutilizacao de base comum de dados para manter a suite legivel

## Etapa 15 - Documentacao dos Testes

- criacao de documento tecnico para explicar estrategia e cobertura da suite
- integracao da documentacao de testes ao indice principal do projeto

## Etapa 16 - Inicio da Camada de Servico

- criacao de servico para registro de entrega de EPI
- centralizacao inicial de validacoes explicitas de negocio
- preparacao da arquitetura para formularios, views e fluxo web

## Etapa 17 - Formulario de Entrega

- criacao do formulario de entrega de EPI
- filtragem de funcionarios ativos
- filtragem de lotes com saldo disponivel
- testes iniciais do formulario

## Etapa 18 - Fluxo Web Inicial de Entrega

- criacao de view protegida por autenticacao
- criacao da rota da app para registrar entrega
- criacao de template inicial do fluxo
- integracao do fluxo web com o service de entrega

## Etapa 19 - Acesso e Login

- ativacao das URLs de autenticacao do Django
- criacao de template inicial de login
- configuracao de redirecionamento apos autenticacao

## Etapa 20 - Melhoria da Tela de Entrega

- reorganizacao visual do template de entrega
- exibicao mais clara de mensagens e erros de validacao
- melhoria de labels, help texts e placeholders do formulario
- uso de campo `datetime-local` para facilitar o preenchimento
- ampliacao dos testes da interface e do formulario

## Uso Deste Documento
Este arquivo deve ser atualizado a cada etapa relevante para manter o registro da evolucao tecnica e funcional do projeto.
