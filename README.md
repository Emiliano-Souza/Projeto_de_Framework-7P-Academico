# Sistema Web de Gestao de Entrega de EPIs

Projeto academico desenvolvido para a disciplina de Desenvolvimento de Software Baseado em Frameworks — curso de Sistemas de Informacao.

---

## Descricao do Projeto

Sistema web para automatizar o controle e gerenciamento de Equipamentos de Protecao Individual (EPIs). Permite o cadastro de funcionarios e equipamentos, controle de estoque em tempo real, monitoramento de validades, registro historico de entregas, devolucoes e baixas, com rastreabilidade completa por movimentacao de estoque.

---

## Framework Utilizado

**Django 5.2 (Python 3.12)**

Django e um framework web de alto nivel escrito em Python que incentiva o desenvolvimento rapido e o design limpo e pragmatico. E amplamente utilizado para sistemas web corporativos, APIs REST, plataformas de conteudo e sistemas de gestao.

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
