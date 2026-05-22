# Sistema Web de Gestao de Entrega de EPIs

Projeto academico desenvolvido para a disciplina de Desenvolvimento de Software Baseado em Frameworks — curso de Sistemas de Informacao.

---

## Descricao do Projeto

Sistema web para automatizar o controle e gerenciamento de Equipamentos de Protecao Individual (EPIs). Permite o cadastro de funcionarios e equipamentos, controle de estoque em tempo real, monitoramento de validades, registro historico de entregas, devolucoes e baixas, com rastreabilidade completa por movimentacao de estoque.

---

## Framework Utilizado

**Django 5.2 (Python 3.12)**

Django e um framework web de alto nivel escrito em Python que incentiva o desenvolvimento rapido e o design limpo e pragmatico. E amplamente utilizado para sistemas web corporativos, APIs REST, plataformas de conteudo e sistemas de gestao.


### Contexto Historico do Django

O Django surgiu em **2003**, dentro da equipe de desenvolvimento web do jornal **Lawrence Journal-World**, em Lawrence, Kansas, nos Estados Unidos. O framework foi criado em um ambiente de redacao, onde havia necessidade de desenvolver sistemas web rapidamente, com prazos curtos, muito conteudo dinamico e forte dependencia de banco de dados.

O projeto foi desenvolvido inicialmente por profissionais como **Adrian Holovaty** e **Simon Willison**, e foi disponibilizado publicamente como software livre em **2005**. O nome Django e uma homenagem ao musico de jazz **Django Reinhardt**.

### Por que o Django foi criado?

O principal objetivo do Django era permitir a criacao rapida de aplicacoes web robustas, seguras e organizadas. Como nasceu em um contexto jornalistico, o framework precisava atender demandas como:

- Publicar conteudo dinamico com agilidade
- Trabalhar bem com bancos de dados relacionais
- Evitar repeticao de codigo
- Facilitar manutencao por equipes
- Entregar sistemas completos em prazos curtos
- Padronizar boas praticas de desenvolvimento web

Por isso, Django ficou conhecido pela filosofia **"The web framework for perfectionists with deadlines"**, ou seja, um framework para quem precisa entregar rapido sem abrir mao de qualidade, organizacao e seguranca.

### Intuito do Framework

O intuito do Django e oferecer uma estrutura completa para desenvolvimento web, reduzindo a necessidade de criar tudo do zero. Ele segue a ideia de **"batteries included"**, trazendo recursos importantes ja integrados ao framework, como:

- ORM para comunicacao com banco de dados usando classes Python
- Sistema de rotas e views
- Templates HTML dinamicos
- Painel administrativo automatico
- Autenticacao de usuarios
- Sistema de permissoes
- Formularios e validacoes
- Protecoes de seguranca contra ataques comuns
- Suporte a testes automatizados

No contexto deste projeto, isso foi importante porque o sistema de entrega de EPIs exige cadastro, controle de estoque, regras de movimentacao, historico, permissoes por perfil e uma interface administrativa funcional.

### Particularidades do Django

Algumas caracteristicas que diferenciam o Django de outros frameworks sao:

- **Arquitetura MVT**: Django usa Model, View e Template, uma variacao do MVC tradicional.
- **Admin automatico**: a partir dos models, o Django gera um painel administrativo completo.
- **ORM integrado**: permite trabalhar com tabelas do banco como classes Python.
- **Alta produtividade**: muitas funcionalidades comuns ja vem prontas.
- **Seguranca nativa**: possui protecoes contra CSRF, XSS, SQL Injection e Clickjacking.
- **Sistema modular por apps**: o projeto pode ser dividido em aplicacoes independentes.
- **Templates proprios**: utiliza a Django Template Language (DTL), com variaveis, tags, filtros e heranca de templates.
- **Migracoes de banco**: alteracoes nos models podem ser transformadas em migracoes versionadas.
- **Foco em manutencao**: incentiva codigo organizado, reaproveitavel e com baixo acoplamento.

### Django Template Language (DTL)

A camada de templates do Django permite criar paginas HTML dinamicas sem misturar diretamente a regra de negocio com a apresentacao. Os templates usam delimitadores especificos para variaveis, tags e comentarios.

#### Delimitadores principais

| Recurso | Delimitador | Funcao |
|---|---|---|
| Variavel | `{{ variavel }}` | Exibe um valor recebido da view |
| Tag | `{% tag %}` | Executa uma instrucao do template |
| Comentario | `{# comentario #}` | Comentario de uma linha no template |
| Bloco de comentario | `{% comment %} ... {% endcomment %}` | Comentario de multiplas linhas |

#### Exemplo de variavel

```html
<h1>{{ funcionario.nome }}</h1>
<p>Setor: {{ funcionario.setor.nome }}</p>
```

Nesse exemplo, o template acessa os dados de um funcionario enviados pela view.

#### Exemplo de condicional

```html
{% if lote.esta_vencido %}
    <span class="badge vencido">Lote vencido</span>
{% else %}
    <span class="badge valido">Lote valido</span>
{% endif %}
```

A tag `{% if %}` permite exibir conteudos diferentes conforme uma condicao.

#### Exemplo de repeticao

```html
<ul>
    {% for entrega in entregas %}
        <li>{{ entrega.funcionario.nome }} - {{ entrega.epi.nome }}</li>
    {% empty %}
        <li>Nenhuma entrega registrada.</li>
    {% endfor %}
</ul>
```

A tag `{% for %}` percorre listas enviadas pela view. O bloco `{% empty %}` e exibido quando a lista esta vazia.

#### Exemplo de filtros

```html
<p>Data da entrega: {{ entrega.data_entrega|date:"d/m/Y" }}</p>
<p>Nome: {{ funcionario.nome|upper }}</p>
```

Filtros modificam a forma como um valor e exibido. No exemplo acima, `date` formata a data e `upper` mostra o texto em letras maiusculas.

#### Exemplo de heranca de template

Arquivo `base.html`:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <title>{% block title %}Sistema de EPIs{% endblock %}</title>
</head>
<body>
    <header>Controle de Entrega de EPIs</header>

    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

Arquivo `dashboard.html`:

```html
{% extends "epi/base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
    <h1>Dashboard</h1>
    <p>Total de funcionarios ativos: {{ total_funcionarios }}</p>
{% endblock %}
```

A heranca de templates evita repeticao de codigo HTML e facilita a padronizacao visual do sistema.

#### Exemplo de URL dinamica

```html
<a href="{% url 'epi:funcionario_detalhe' funcionario.id %}">
    Ver detalhes
</a>
```

A tag `{% url %}` evita escrever rotas fixas diretamente no HTML, deixando o sistema mais facil de manter.

### Exemplo de Sintaxe Django no Projeto

Exemplo simplificado de um model:

```python
from django.db import models

class EPI(models.Model):
    nome = models.CharField(max_length=100)
    ca = models.CharField(max_length=30, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
```

Exemplo simplificado de uma view:

```python
from django.shortcuts import render
from .models import EPI

def lista_epis(request):
    epis = EPI.objects.filter(ativo=True)
    return render(request, "epi/lista_epis.html", {"epis": epis})
```

Exemplo simplificado de template:

```html
<h1>EPIs Ativos</h1>

<ul>
    {% for epi in epis %}
        <li>{{ epi.nome }} - CA: {{ epi.ca }}</li>
    {% empty %}
        <li>Nenhum EPI ativo cadastrado.</li>
    {% endfor %}
</ul>
```

Esse fluxo mostra a ideia central do Django: o **Model** representa os dados, a **View** busca e prepara as informacoes, e o **Template** apresenta o resultado em HTML.

### Por que Django?

- ORM poderoso com suporte nativo a migrações de banco
- Admin nativo gerado automaticamente a partir dos models
- Sistema de autenticacao e permissoes integrado
- Arquitetura MVT (Model-View-Template) bem definida
- Ecossistema maduro e documentacao extensa
- Facilidade para aplicar boas praticas desde o inicio

### Arquitetura MVT

O projeto segue o padrao MVT nativo do Django:

- **Model** — `epi/models.py`: entidades, constraints e integridade do banco
- **View** — `epi/views/`: logica HTTP, autenticacao e orquestracao
- **Template** — `epi/templates/epi/`: camada de apresentacao HTML

Alem do MVT padrao, o projeto adota uma camada de **Service** (`epi/services/`) para isolar as regras de negocio operacionais fora das views e dos models.

### Diferencias em relacao ao Laravel

| Aspecto | Django (Python) | Laravel (PHP) |
|---|---|---|
| Linguagem | Python | PHP |
| ORM | Django ORM (nativo) | Eloquent |
| Admin | Gerado automaticamente | Requer pacote externo (ex: Filament) |
| Migrations | `makemigrations` + `migrate` | `make:migration` + `migrate` |
| Autenticacao | Nativo e integrado | Via Laravel Breeze/Sanctum |
| Templates | Django Template Language | Blade |
| Estrutura | App-based (modular) | MVC com pastas fixas |
| Filosofia | "Batteries included" | Flexivel e expressivo |

### Pontos Positivos

- Admin nativo elimina necessidade de construir CRUD basico
- ORM com suporte a constraints, validacoes e transacoes
- Sistema de grupos e permissoes pronto para uso
- Testes automatizados integrados com banco temporario
- Paginacao, mensagens e formularios nativos
- Documentacao oficial excelente

### Dificuldades Encontradas

- Curva inicial para entender o ciclo de vida do ORM e o `save()` customizado
- Configuracao do ambiente Docker com CRLF no `entrypoint.sh`
- Entender a diferenca entre `CheckConstraint` (banco) e `clean()` (aplicacao)
- Organizar a camada de service sem quebrar a compatibilidade com o admin

### Usaria Novamente?

Sim. Django se mostrou uma escolha solida para sistemas de gestao com regras de negocio complexas. A combinacao de ORM robusto, admin nativo, autenticacao integrada e testes automatizados reduziu significativamente o tempo de desenvolvimento das partes estruturais do sistema.

---

## Tecnologias

- Python 3.12
- Django 5.2
- PostgreSQL 16
- Docker e Docker Compose

---

## Como Executar

### Pre-requisitos

- Docker Desktop instalado e rodando

### 1. Subir o ambiente

```powershell
cd Projeto
docker compose up --build
```

Aguarde a mensagem `Subindo servidor...` no terminal.

### 2. Criar grupos e popular dados

Em outro terminal:

```powershell
docker compose exec django python manage.py criar_grupos
docker compose exec django python manage.py seed
```

### 3. Acessar o sistema

Abra `http://localhost:8000/` e faca login com um dos usuarios abaixo:

| Usuario | Senha | Perfil |
|---|---|---|
| `admin` | `admin` | Acesso total + painel admin |
| `almoxarife` | `almoxarife` | Operacoes: entrega, devolucao e baixa |
| `gestor` | `gestor` | Somente consulta |

### 4. Rodar os testes

```powershell
docker compose exec django python manage.py test
```

---

## Funcionalidades

### Dashboard
Tela inicial com indicadores operacionais: funcionarios ativos, EPIs cadastrados, lotes com saldo, entregas pendentes e alertas de lotes vencidos ou proximos do vencimento.

### Listagens
- Funcionarios com busca por nome e matricula, filtro por setor e status
- Historico completo de entregas por funcionario
- EPIs com busca e filtro por status
- Lotes com destaque visual para lotes vencidos
- Entregas com filtro por status e funcionario
- Historico de movimentacoes de estoque paginado

### Operacoes (Almoxarife e Administrador)
- Registrar entrega de EPI para funcionario
- Registrar devolucao parcial ou total
- Registrar baixa com motivo (danificado, extraviado, vencido, descartado)

### Cadastro, Edicao e Exclusao (Admin nativo)
Acesse `http://localhost:8000/admin/` com o usuario `admin` para gerenciar:
- Setores
- Funcionarios
- EPIs
- Lotes
- Entregas
- Movimentacoes

### Autenticacao e Permissoes
- Login/logout com sessao de 1 hora
- 3 perfis: Administrador, Almoxarife e Gestor
- Tela de acesso negado (403) para rotas restritas
- Navbar adaptada ao perfil do usuario

---

## Estrutura do Projeto

```
Projeto/
├── config/          # Configuracoes globais do Django
├── epi/             # App principal do dominio
│   ├── models.py    # Entidades e integridade
│   ├── forms.py     # Formularios web
│   ├── views/       # Camada HTTP
│   ├── services/    # Regras de negocio
│   ├── urls/        # Rotas por fluxo
│   ├── templates/   # Templates HTML
│   ├── static/      # CSS compartilhado
│   ├── tests/       # Suite de testes
│   └── management/  # Comandos customizados
├── docs/            # Documentacao tecnica
└── docker-compose.yml
```

---

## Documentacao Tecnica

A documentacao completa esta na pasta `docs/`:

- `como_rodar.md` — tutorial de execucao
- `arquitetura.md` — visao geral da arquitetura
- `estrutura_django.md` — organizacao do projeto no Django
- `regras_de_negocio.md` — regras funcionais do sistema
- `banco_de_dados.md` — modelagem e decisoes do banco
- `fluxos_aplicacao.md` — fluxos de entrega, devolucao e baixa
- `testes.md` — estrategia e cobertura de testes
- `decisoes_tecnicas.md` — justificativas das escolhas
- `guia_tecnico.md` — snippets e pontos de manutencao

---

## Autores

- **Emiliano Ferreira de Souza Junior**
- **Mario Alves Fernandes Neto**

---

*Projeto academico — curso de Sistemas de Informacao.*
