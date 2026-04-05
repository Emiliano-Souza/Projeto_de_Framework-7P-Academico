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
LOGIN_REDIRECT_URL = "epi:registrar_entrega"
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

- `views/entregas.py`
- `views/devolucoes.py`
- `views/baixas.py`

Cada view:

- exige autenticacao
- instancia formulario
- chama o service correspondente
- trata `ValidationError`
- exibe mensagens de sucesso ou erro

### `Projeto/epi/urls/`
Rotas separadas por fluxo:

- `urls/entregas.py`
- `urls/devolucoes.py`
- `urls/baixas.py`

Essa separacao evita que um unico arquivo cresca demais conforme o projeto evolui.

### `Projeto/epi/templates/epi/`
Templates HTML dos fluxos web:

- `registrar_entrega.html`
- `registrar_devolucao.html`
- `registrar_baixa.html`

Os templates atuais priorizam:

- clareza da operacao
- mensagens de erro e sucesso
- navegacao basica entre fluxos

### `Projeto/epi/tests/`
Suite de testes separada por responsabilidade:

- cadastros
- lotes
- entrada e saida
- movimentacoes
- formularios
- views

Essa organizacao ajuda a manter cobertura tecnica sem concentrar tudo em um unico arquivo.

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

## Particularidades Importantes do Projeto

### 1. A regra principal nao fica mais escondida na view
As views apenas orquestram request e response.

### 2. A regra operacional nao fica mais toda no model
O model ainda participa, mas a camada de service passou a concentrar a regra critica.

### 3. O admin continua funcionando
Mesmo com service, a sobrescrita de `save()` em `EntregaEPI` preserva coerencia quando o registro e salvo por ORM ou admin.

### 4. O banco real pode divergir do codigo se `migrate` nao for executado
Os testes usam banco temporario. Por isso, rodar teste com sucesso nao substitui aplicar migracao no banco real do container.

## Resumo
Para um dev novo no projeto, a leitura recomendada e:

1. `docs/estrutura_django.md`
2. `docs/fluxos_aplicacao.md`
3. `docs/guia_tecnico.md`
4. `Projeto/epi/services/entregas.py`
5. `Projeto/epi/tests/`
