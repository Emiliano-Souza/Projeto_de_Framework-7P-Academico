# Decisoes Tecnicas

## 1. Separacao entre banco e aplicacao
Decisao:
Executar PostgreSQL e Django em containers separados.

Motivo:
Essa abordagem melhora organizacao da infraestrutura, facilita manutencao e reduz conflitos de responsabilidade.

## 2. Porta externa do PostgreSQL fora do padrao
Decisao:
Publicar o PostgreSQL na porta `55432` no host local.

Motivo:
Reduz o risco de conflito com outra instalacao local de PostgreSQL usando a porta `5432`.

## 3. Uso de healthcheck no servico do banco
Decisao:
Adicionar `healthcheck` com `pg_isready` no servico `db`.

Motivo:
Permite verificar se o PostgreSQL esta realmente pronto para aceitar conexoes.

## 4. Criacao de uma app de dominio para o sistema
Decisao:
Centralizar a modelagem inicial do dominio em uma app Django dedicada.

Motivo:
Melhora a organizacao do projeto e agrupa modelos, admin e migracoes em um unico modulo funcional.

## 5. Construir primeiro a camada de banco
Decisao:
Evoluir o sistema em etapas, com foco inicial na modelagem do banco antes das telas.

Motivo:
Isso reduz retrabalho, torna a regra de negocio mais clara e facilita documentacao tecnica consistente.

## 6. Migrar gradualmente a regra operacional para services
Decisao:
Mover a orquestracao de entrega, devolucao e baixa para camada de service, mantendo compatibilidade com o model.

Motivo:

- deixa a regra mais explicita
- melhora testabilidade
- evita acoplamento excessivo nas views
- preserva consistencia no admin e no ORM

## 7. Manter `EntregaEPI` como entidade operacional central
Decisao:
Usar `EntregaEPI` como ponto central para entrega, devolucao e baixa.

Motivo:

- simplifica a rastreabilidade
- facilita o uso de deltas
- evita criar tabelas de operacao separadas cedo demais

## 8. Usar `MovimentacaoEstoque` como trilha unica de auditoria
Decisao:
Toda operacao relevante de estoque deve gerar uma linha em `movimentacao_estoque`.

Motivo:

- melhora auditoria
- centraliza historico
- facilita tela de rastreabilidade
- fortalece o projeto academicamente

## 9. Separar views e URLs por fluxo funcional
Decisao:
Organizar a camada web em modulos como `views/entregas.py`, `views/devolucoes.py`, `views/baixas.py` e equivalentes em `urls/`.

Motivo:

- evita arquivos monoliticos
- deixa a navegacao no codigo mais clara
- prepara o projeto para crescer sem bagunca

## 10. Usar filtros de queryset nos formularios
Decisao:
Deixar os formularios mostrarem apenas opcoes operacionais validas.

Motivo:

- melhora a UX
- reduz erro humano
- complementa, sem substituir, a validacao do service

## 11. Tratar baixa sem alterar saldo do lote
Decisao:
Registrar baixa como encerramento de quantidade entregue sem retorno fisico ao estoque.

Motivo:

- o lote ja foi reduzido no momento da entrega
- a baixa eh um evento operacional, nao uma devolucao
- isso preserva o sentido correto do saldo do lote

## 13. CSS e Templates Padronizados pelo Django
Decisao:
Extrair todo o CSS dos templates para um arquivo estatico unico em `epi/static/epi/epi.css`, seguindo a convencao de pastas do Django (`<app>/static/<app>/`).

Motivo:

- elimina duplicacao de estilos entre templates
- facilita manutencao visual centralizada
- segue o padrao nativo do `django.contrib.staticfiles`
- dispensa configuracao manual de `STATICFILES_DIRS`

## 14. Navbar como Componente Reutilizavel
Decisao:
Extrair a barra de navegacao para `templates/epi/navbar.html` e incluir via `{% include %}` em todos os templates.

Motivo:

- elimina duplicacao de HTML de navegacao
- centraliza manutencao da navbar em um unico arquivo
- usa `request.path` para detectar o link ativo dinamicamente

## 15. URLs via `{% url %}` nos Templates
Decisao:
Substituir todas as URLs hardcoded nos templates pelo tag `{% url 'namespace:name' %}` do Django.

Motivo:

- evita quebra silenciosa quando rotas mudam
- segue a convencao padrao do Django
- centraliza a definicao de rotas nos arquivos `urls/`

## 16. Helper Centralizado de ValidationError nas Views
Decisao:
Extrair o bloco `try/except ValidationError` repetido nas 3 views para um helper em `views/utils.py`.

Motivo:

- elimina duplicacao de codigo entre views
- facilita manutencao e evolucao do tratamento de erros
- mantem as views limpas e focadas no fluxo HTTP

## 17. Paginacao na Tela de Movimentacoes
Decisao:
Adicionar `Paginator` do Django na view de movimentacoes com 50 itens por pagina.

Motivo:

- evita carregamento de todos os registros em memoria
- melhora performance conforme o volume de dados cresce
- usa o mecanismo nativo do Django sem dependencias externas

## 18. Template Base Compartilhado
Decisao:
Criar `epi/base.html` com a estrutura HTML comum e fazer todos os templates estenderem via `{% extends %}`.

Motivo:

- elimina repeticao de `<!DOCTYPE>`, `<head>`, `{% load static %}` e `{% include navbar %}` em cada template
- qualquer mudanca estrutural e feita em um unico lugar
- segue o padrao nativo de heranca de templates do Django
- o `login.html` tambem estende o mesmo base, mantendo visual consistente

## 19. Grupos e Permissoes via Decorador Customizado
Decisao:
Usar grupos nativos do Django (`Group`) com um decorador `grupo_required` customizado em vez de `@permission_required` por permissao individual.

Motivo:

- mais legivel: `@grupo_required("Almoxarife")` e mais claro que listar permissoes individuais
- mais facil de manter: adicionar ou remover acesso e feito no grupo, nao no codigo
- superusuario sempre passa, sem necessidade de atribuir grupos manualmente
- retorna 403 com template proprio em vez de redirecionar para login

## 20. Context Processor para Perfil do Usuario
Decisao:
Injetar `pode_operar` em todos os templates via context processor em vez de verificar grupos diretamente no template.

Motivo:

- templates ficam limpos e sem logica de negocio
- a regra de quem pode operar fica centralizada em um unico lugar
- facil de evoluir: basta alterar o context processor

## 21. Seed como Comando Django
Decisao:
Implementar os dados de demonstracao como um management command (`python manage.py seed`) em vez de fixture.

Motivo:

- usa os services reais, garantindo que as regras de negocio sejam respeitadas
- gera movimentacoes de estoque reais junto com os dados
- idempotente: pode ser rodado multiplas vezes sem duplicar dados
- mais facil de manter e evoluir do que um arquivo JSON de fixture

## 12. Manter documentacao tecnica junto da evolucao do codigo
Decisao:
Atualizar a documentacao a cada etapa importante do projeto.

Motivo:

- evita documentacao desatualizada
- ajuda onboarding tecnico
- melhora apresentacao e manutencao
