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

## Etapa 21 - Reorganizacao de Views e Rotas

- separacao das views da app em pasta `views/`
- separacao das rotas da app em pasta `urls/`
- criacao do modulo `views/entregas.py` para o fluxo de entrega
- criacao do modulo `urls/entregas.py` para as rotas do fluxo de entrega
- manutencao das URLs e nomes existentes sem alterar comportamento

## Etapa 22 - Formulario de Devolucao

- criacao do formulario inicial de devolucao de EPI
- filtragem para exibir apenas entregas com devolucao pendente
- preparacao da interface com labels, help texts e campos padronizados
- ampliacao dos testes para validar a estrutura do novo formulario

## Etapa 23 - Servico de Devolucao e Refino da Camada de Servico

- criacao do servico para registrar devolucao de EPI
- validacao de entrega existente, quantidade positiva e saldo pendente para devolucao
- centralizacao da orquestracao de lote e movimentacao na camada de servico
- ajuste do model para delegar persistencia operacional ao service
- ampliacao dos testes para cobrir devolucoes validas e invalidas via service

## Etapa 24 - Fluxo Web de Devolucao

- criacao da view protegida por autenticacao para devolucao de EPI
- criacao da rota dedicada ao fluxo de devolucao
- criacao do template inicial da tela de devolucao
- exibicao de mensagens de sucesso e erro no fluxo web
- ampliacao dos testes para validar acesso, renderizacao e submissao da devolucao

## Etapa 25 - Estrutura Inicial da Baixa

- adicao do campo `quantidade_baixada` em `entrega_epi`
- adicao de regra para limitar devolucao mais baixa a quantidade entregue
- preparacao do tipo de movimentacao `baixa` em `movimentacao_estoque`
- ampliacao dos testes para validar a nova integridade estrutural
- criacao da migracao inicial da estrutura de baixa

## Etapa 26 - Formulario de Baixa

- criacao do formulario inicial de baixa de EPI
- filtragem para exibir apenas entregas com saldo em aberto para baixa
- padronizacao dos motivos de baixa no formulario
- preparacao da interface com labels, help texts e campos padronizados
- ampliacao dos testes para validar a estrutura do novo formulario

## Etapa 27 - Servico de Baixa

- criacao do servico para registrar baixa de EPI
- validacao de entrega existente, quantidade positiva, motivo obrigatorio e saldo em aberto
- garantia de que a baixa nao aumenta o estoque do lote
- geracao de movimentacao do tipo `baixa` com motivo operacional
- ampliacao dos testes para cobrir baixas validas e invalidas

## Etapa 28 - Fluxo Web de Baixa

- criacao da view protegida por autenticacao para baixa de EPI
- criacao da rota dedicada ao fluxo de baixa
- criacao do template inicial da tela de baixa
- exibicao de mensagens de sucesso e erro no fluxo web
- ampliacao dos testes para validar acesso, renderizacao e submissao da baixa

## Etapa 29 - Reforco da Documentacao Tecnica

- criacao de documentacao especifica para estrutura Django
- criacao de documentacao tecnica dos fluxos de aplicacao
- criacao de guia tecnico com snippets e particularidades do projeto
- atualizacao do README com foco maior em onboarding tecnico
- atualizacao da documentacao de testes para refletir o estado atual da suite

## Etapa 30 - Aprofundamento da Documentacao para Dev

- detalhamento de dependencias entre modulos do Django
- detalhamento do fluxo interno de persistencia com transacao e lock
- registro explicito de invariantes do dominio
- inclusao de troubleshooting tecnico recorrente
- inclusao de checklist tecnico para evolucao de novas funcionalidades

## Etapa 31 - Anatomia do Service Principal

- criacao de documentacao dedicada ao arquivo `services/entregas.py`
- explicacao funcao por funcao da camada de service principal
- detalhamento do fluxo interno de persistencia e criacao de movimentacoes
- destaque dos pontos mais sensiveis para manutencao e refatoracao

## Etapa 32 - Movimentacao de Entrada de Lote

- criacao de service para registrar entrada de lote com usuario responsavel
- geracao automatica de `movimentacao_estoque` do tipo `entrada`
- ampliacao dos testes para validar entrada rastreavel de lote
- atualizacao da documentacao tecnica para refletir a rastreabilidade da entrada

## Etapa 33 - Tela de Historico de Movimentacoes

- criacao da view protegida por autenticacao para listar movimentacoes
- criacao da rota dedicada ao historico do estoque
- criacao do template inicial da listagem de movimentacoes
- exibicao dos principais campos de rastreabilidade em tabela
- ampliacao dos testes para validar acesso, estado vazio e exibicao do historico

## Etapa 34 - Revisao Geral da Documentacao

- alinhamento da arquitetura ao estado atual do projeto
- atualizacao da configuracao do ambiente com rotas e rotina real de uso
- ampliacao das decisoes tecnicas com a camada de service e rastreabilidade
- ajuste das regras de negocio para refletir entrada, entrega, devolucao e baixa
- sincronizacao final da documentacao com os fluxos e telas atuais

## Etapa 35 - Consolidacao das Regras de Negocio

- reforco da validacao explicita de quantidade positiva no service de entrega
- ampliacao dos testes para cobrir entrega com quantidade zero e negativa
- ajuste da documentacao para refletir a consolidacao das regras do service

## Etapa 36 - Correcoes de Infraestrutura e Dominio

- `docker-compose.yml` atualizado para usar `depends_on: condition: service_healthy` no servico Django
- `entrypoint.sh` atualizado com logs intermediarios de migrations e subida do servidor
- `clean()` adicionado em `MovimentacaoEstoque` para validar `quantidade > 0` e `quantidade_depois >= 0` via `full_clean()`
- campo `usuario_baixa` adicionado em `EntregaEPI` para separar o responsavel pela baixa do responsavel pela devolucao
- `registrar_baixa_epi` atualizado para usar `usuario_baixa` em vez de `usuario_devolucao`
- migracao `0009_entrega_epi_usuario_baixa` criada
- documentacao atualizada para refletir todas as correcoes

## Etapa 37 - Padronizacao da Camada Web

- CSS extraido dos templates para `epi/static/epi/epi.css` seguindo convencao do Django
- `STATICFILES_DIRS` removido do `settings.py` — desnecessario com a convencao `<app>/static/<app>/`
- navbar extraida para componente `templates/epi/navbar.html` incluido via `{% include %}`
- link ativo na navbar detectado dinamicamente via `request.path`
- todas as URLs hardcoded nos templates substituidas por `{% url %}`
- bloco `try/except ValidationError` duplicado nas views extraido para `views/utils.py`
- `Paginator` adicionado na view de movimentacoes com 50 itens por pagina
- bloco `DATABASES` SQLite morto removido do `settings.py`
- documentacao atualizada para refletir todas as mudancas

## Etapa 38 - Template Base e Padronizacao de Login

- `epi/base.html` criado com estrutura HTML, `{% load static %}`, link do CSS e inclusao da navbar
- todos os templates refatorados para `{% extends "epi/base.html" %}` com `{% block content %}`
- `login.html` refatorado para estender `epi/base.html`, mantendo visual consistente
- `AUTH_PASSWORD_VALIDATORS` esvaziado para facilitar criacao de usuarios em desenvolvimento
- documentacao atualizada

## Etapa 39 - Seed de Dados de Demonstracao

- comando `python manage.py seed` criado em `management/commands/seed.py`
- cria 5 setores, 15 funcionarios (13 ativos, 2 inativos), 8 EPIs, 10 lotes
- 1 lote vencido e 1 proximo do vencimento para demonstrar alertas
- 10 entregas, 1 devolucao parcial e 1 baixa
- usuarios admin, almoxarife e gestor criados com senhas simples

## Etapa 40 - Dashboard

- view `dashboard_view` criada em `views/dashboard.py`
- rota `""` (raiz) mapeada para o dashboard
- `LOGIN_REDIRECT_URL` alterado para `epi:dashboard`
- template `dashboard.html` com cards de indicadores e tabela de ultimas movimentacoes
- indicadores: funcionarios ativos, EPIs, lotes com saldo, entregas pendentes, lotes vencidos, proximos do vencimento, estoque abaixo do minimo
- navbar atualizada com link Dashboard

## Etapa 41 - Grupos e Permissoes

- comando `python manage.py criar_grupos` criado em `management/commands/criar_grupos.py`
- 3 grupos definidos: Administrador (todas as permissoes), Almoxarife (operacoes), Gestor (somente consulta)
- decorador `grupo_required` criado em `views/utils.py`
- views de entrega, devolucao e baixa protegidas com `@grupo_required("Administrador", "Almoxarife")`
- context processor `perfil_usuario` criado em `context_processors.py` injetando `pode_operar`
- navbar exibe links de operacao condicionalmente via `pode_operar`
- template `acesso_negado.html` criado para resposta 403
- seed atualizado para criar usuarios almoxarife e gestor com grupos atribuidos

## Uso Deste Documento
Este arquivo deve ser atualizado a cada etapa relevante para manter o registro da evolucao tecnica e funcional do projeto.
