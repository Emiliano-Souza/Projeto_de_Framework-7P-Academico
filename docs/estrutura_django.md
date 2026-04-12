# Estrutura Django

## Objetivo
Este documento explica como o projeto esta organizado dentro do Django e onde cada responsabilidade tecnica esta localizada.

## Mapa Geral
O projeto esta dividido em duas camadas principais:

- `Projeto/config`: configuracao global do projeto Django
- `Projeto/epi`: app de dominio da gestao de EPIs

Essa separacao segue a estrutura padrao do Django:

- `project`: configuracoes, URLs principais e settings
- `app`: dominio funcional da aplicacao

## Projeto Django

### `Projeto/manage.py`
Ponto de entrada dos comandos administrativos do Django.

Exemplos:

```powershell
python manage.py migrate
python manage.py test
python manage.py createsuperuser
```

### `Projeto/config/settings.py`
Concentrador das configuracoes globais.

Pontos importantes deste projeto:

- PostgreSQL configurado como banco principal
- `DEFAULT_AUTO_FIELD` definido para `BigAutoField`
- pasta global de templates habilitada
- autenticacao padrao do Django habilitada

Trecho relevante:

```python
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = "epi:dashboard"
```

### `Projeto/config/urls.py`
Arquivo que conecta as rotas globais do sistema.

Hoje ele expande principalmente:

- admin do Django
- rotas da app `epi`
- rotas de autenticacao do Django

Trecho relevante:

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("epi.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
```

## App `epi`

### `Projeto/epi/models.py`
Define as entidades centrais do dominio:

- `Setor`
- `Funcionario`
- `EPI`
- `EPILote`
- `EntregaEPI`
- `MovimentacaoEstoque`

Pontos importantes:

- o model `EntregaEPI` ainda existe como centro do dominio
- a persistencia operacional delega para a camada de servico
- constraints importantes ficam no proprio model

Trecho relevante:

```python
def save(self, *args, **kwargs):
    from epi.services.entregas import persistir_entrega_epi

    return persistir_entrega_epi(self, *args, **kwargs)
```

Essa decisao foi adotada para manter compatibilidade com:

- admin do Django
- criacao direta por ORM
- regras de negocio centralizadas em service

### `Projeto/epi/forms.py`
Concentra os formularios web.

Hoje existem formularios para:

- entrega
- devolucao
- baixa

Eles fazem validacao de entrada e filtros de queryset para melhorar a interface.

Trecho relevante:

```python
self.fields["entrega"].queryset = (
    EntregaEPI.objects.select_related("funcionario", "epi_lote", "epi_lote__epi")
    .filter(quantidade_devolvida__lt=(F("quantidade_entregue") - F("quantidade_baixada")))
    .order_by("-data_entrega", "-id")
)
```

Esse tipo de filtro evita que a tela mostre registros invalidos para a operacao.

### `Projeto/epi/services/entregas.py`
Camada de servico do dominio.

Hoje ela concentra:

- `registrar_entrega_epi`
- `registrar_devolucao_epi`
- `registrar_baixa_epi`
- `persistir_entrega_epi`

Ela eh a peca mais importante do desenho atual, porque faz a orquestracao de:

- validacao de negocio
- atualizacao de entrega
- atualizacao de lote
- movimentacao de estoque
- transacao

### `Projeto/epi/views/`
Views organizadas por dominio funcional:

- `views/dashboard.py`: view do dashboard com indicadores e alertas operacionais
- `views/funcionarios.py`: listagem de funcionarios e historico por funcionario
- `views/epis.py`: listagem de EPIs e listagem de lotes
- `views/entregas.py`: formulario de registro de entrega
- `views/entregas_lista.py`: listagem de entregas com filtros
- `views/devolucoes.py`: formulario de registro de devolucao
- `views/baixas.py`: formulario de registro de baixa
- `views/movimentacoes.py`: historico paginado de movimentacoes
- `views/utils.py`: helper `aplicar_erros_ao_form` e decorador `grupo_required`

As views de entrega, devolucao e baixa usam `@grupo_required("Administrador", "Almoxarife")` para restringir acesso por perfil.

### `Projeto/epi/urls/`
Rotas separadas por fluxo:

- `urls/dashboard.py`: rota raiz `""`
- `urls/funcionarios.py`: `/funcionarios/` e `/funcionarios/<pk>/`
- `urls/epis.py`: `/epis/` e `/lotes/`
- `urls/entregas.py`: `/entregas/nova/` e `/entregas/`
- `urls/devolucoes.py`: `/devolucoes/nova/`
- `urls/baixas.py`: `/baixas/nova/`
- `urls/movimentacoes.py`: `/movimentacoes/`

Essa separacao evita que um unico arquivo cresca demais conforme o projeto evolui.

### `Projeto/epi/templates/epi/`
Templates HTML dos fluxos web:

- `base.html`: template base compartilhado
- `navbar.html`: exibe links condicionalmente com base no perfil via `pode_operar`
- `alertas.html`: componente reutilizavel de alertas visuais (erro/aviso)
- `dashboard.html`: tela inicial com indicadores operacionais e alertas
- `acesso_negado.html`: tela 403 para acesso sem permissao
- `listar_funcionarios.html`: listagem com busca e filtros
- `historico_funcionario.html`: historico de entregas por funcionario com alerta de itens em aberto
- `listar_epis.html`: listagem de EPIs com busca e filtros
- `listar_lotes.html`: listagem de lotes com destaque para vencidos
- `listar_entregas.html`: listagem de entregas com busca e filtros
- `registrar_entrega.html`
- `registrar_devolucao.html`
- `registrar_baixa.html`
- `listar_movimentacoes.html`

Os templates atuais:

- nao possuem CSS inline nem estrutura HTML repetida
- estendem `base.html` e definem apenas `{% block title %}` e `{% block content %}`
- usam `{% url %}` para todas as rotas, sem URLs hardcoded
- incluem controles de paginacao na tela de movimentacoes

### `Projeto/templates/registration/`
Templates de autenticacao do Django:

- `login.html`: estende `epi/base.html` para manter visual consistente com o restante do sistema

### `Projeto/epi/context_processors.py`
Context processor `perfil_usuario` que injeta `pode_operar` em todos os templates.

- `pode_operar = True` para superusuarios, Administradores e Almoxarifes
- `pode_operar = False` para Gestores e usuarios sem grupo
- usado pela navbar para exibir ou ocultar links de operacao

### `Projeto/epi/management/`
Comandos customizados do Django:

- `management/commands/seed.py`: popula o banco com dados de demonstracao (5 setores, 15 funcionarios, 8 EPIs, 10 lotes, 10 entregas, usuarios admin/almoxarife/gestor)
- `management/commands/criar_grupos.py`: cria os grupos Administrador, Almoxarife e Gestor com suas permissoes

Execucao:

```powershell
docker compose exec django python manage.py criar_grupos
docker compose exec django python manage.py seed
```

### `Projeto/epi/tests/`
Suite de testes separada por responsabilidade:

- `base.py`: setup compartilhado — usuario com grupo Almoxarife, setor, funcionario, EPI e lote
- `test_cadastros.py`: unicidade e comportamento de PROTECT
- `test_lotes.py`: integridade de lotes e service de entrada
- `test_entrada_saida.py`: regras centrais de entrega, devolucao e baixa
- `test_movimentacoes.py`: integridade da auditoria
- `test_forms.py`: filtros e validacao de formularios
- `test_views.py`: autenticacao, renderizacao e submissao web
- `test_permissoes.py`: permissoes por grupo e rollback de transacao com erro

### `Projeto/epi/static/epi/`
Arquivos estaticos da app:

- `epi.css`: folha de estilos unica e compartilhada por todos os templates

O Django descobre essa pasta automaticamente via `django.contrib.staticfiles` sem necessidade de `STATICFILES_DIRS`.

## Fluxo de Dependencia Entre Camadas

O caminho padrao de uma operacao web hoje eh:

1. `URL`
2. `View`
3. `Form`
4. `Service`
5. `Model / ORM`
6. `Banco`

Em termos praticos:

```text
request HTTP
-> urls/
-> views/
-> forms.py
-> services/entregas.py
-> models.py
-> PostgreSQL
```

## Mapa Tecnico de Arquivos

Para leitura rapida do codigo, estes sao os pontos mais importantes:

- `Projeto/config/settings.py`: configuracao global, banco, templates e autenticacao
- `Projeto/config/urls.py`: roteamento principal do projeto
- `Projeto/epi/models.py`: entidades, constraints e delegacao de persistencia
- `Projeto/epi/forms.py`: filtros de interface e validacao de entrada
- `Projeto/epi/services/entregas.py`: regra operacional principal
- `Projeto/epi/views/dashboard.py`: indicadores e alertas operacionais
- `Projeto/epi/views/funcionarios.py`: listagem e historico por funcionario
- `Projeto/epi/views/epis.py`: listagem de EPIs e lotes
- `Projeto/epi/views/entregas_lista.py`: listagem de entregas
- `Projeto/epi/views/utils.py`: helper de erros e decorador grupo_required
- `Projeto/epi/context_processors.py`: injeta perfil do usuario nos templates
- `Projeto/epi/templates/epi/alertas.html`: componente de alertas reutilizavel
- `Projeto/epi/urls/`: agrupamento de rotas por fluxo
- `Projeto/epi/templates/epi/base.html`: template base compartilhado por todos os templates
- `Projeto/epi/templates/epi/navbar.html`: componente de navegacao
- `Projeto/epi/static/epi/epi.css`: estilos compartilhados
- `Projeto/epi/tests/`: validacao automatizada de dominio e interface

## Dependencias Entre Modulos

O desenho atual tenta manter uma direcao clara de dependencias:

- `views` dependem de `forms` e `services`
- `forms` dependem de `models`
- `services` dependem de `models`
- `models` nao dependem de `views`

Existe uma excecao controlada:

- `EntregaEPI.save()` importa o service localmente para delegar persistencia

Essa importacao tardia foi escolhida para:

- evitar circular import no carregamento do modulo
- manter o admin e o ORM coerentes com a regra do dominio

## Convencoes de Organizacao Adotadas

### 1. Agrupar por fluxo funcional
Por isso existem:

- `views/entregas.py`
- `views/devolucoes.py`
- `views/baixas.py`

e:

- `urls/entregas.py`
- `urls/devolucoes.py`
- `urls/baixas.py`

### 2. Manter services orientados a caso de uso
O arquivo `services/entregas.py` hoje concentra mais de um fluxo porque todos giram em torno de `EntregaEPI`. Se a complexidade crescer, um proximo passo natural eh separar em:

- `services/entregas.py`
- `services/devolucoes.py`
- `services/baixas.py`
- `services/persistencia_entrega.py`

### 3. Formularios como filtro tecnico da interface
Os forms nao sao usados apenas para renderizacao; eles reduzem estados invalidos visiveis para o operador.

## Sequencia de Leitura Recomendada para Dev

Se alguem novo entrar no projeto e quiser entender rapido:

1. ler `Projeto/epi/models.py`
2. ler `Projeto/epi/services/entregas.py`
3. ler `Projeto/epi/forms.py`
4. ler `Projeto/epi/views/`
5. ler `Projeto/epi/tests/test_entrada_saida.py`

Essa ordem funciona bem porque vai:

- da estrutura do dominio
- para a regra operacional
- para a interface
- para a validacao automatizada

## Particularidades Importantes do Projeto

### 1. A regra principal nao fica mais escondida na view
As views apenas orquestram request e response.

### 2. A regra operacional nao fica mais toda no model
O model ainda participa, mas a camada de service passou a concentrar a regra critica.

### 3. O admin continua funcionando
Mesmo com service, a sobrescrita de `save()` em `EntregaEPI` preserva coerencia quando o registro e salvo por ORM ou admin.

### 4. O banco real pode divergir do codigo se `migrate` nao for executado
Os testes usam banco temporario. Por isso, rodar teste com sucesso nao substitui aplicar migracao no banco real do container.

### 5. O projeto usa abordagem hibrida entre model e service
Ele nao e um projeto Django "fat models" puro, nem um projeto com dominio 100% fora do ORM.

Hoje a decisao pratica eh:

- integridade estrutural no model
- orquestracao operacional no service
- compatibilidade de persistencia mantida no `save()`

## Resumo
Para um dev novo no projeto, a leitura recomendada e:

1. `docs/estrutura_django.md`
2. `docs/fluxos_aplicacao.md`
3. `docs/guia_tecnico.md`
4. `Projeto/epi/services/entregas.py`
5. `Projeto/epi/tests/`
