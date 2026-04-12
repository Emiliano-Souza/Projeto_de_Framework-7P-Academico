# Como Rodar o Projeto

Este guia explica como subir o ambiente do zero, popular os dados e acessar o sistema.

## Pre-requisitos

- Docker Desktop instalado e rodando
- Git (para clonar o repositorio, se necessario)

## Passo 1 — Entrar na pasta do projeto

```powershell
cd Projeto
```

## Passo 2 — Subir os containers

```powershell
docker compose up --build
```

Aguarde ate ver no terminal:

```
Banco pronto.
Rodando migrations...
Subindo servidor...
```

O sistema estara disponivel em `http://localhost:8000`.

## Passo 3 — Criar os grupos de permissao

Em outro terminal, com os containers rodando:

```powershell
docker compose exec django python manage.py criar_grupos
```

## Passo 4 — Popular os dados de demonstracao

```powershell
docker compose exec django python manage.py seed
```

Isso cria automaticamente:

- 5 setores
- 15 funcionarios (13 ativos, 2 inativos)
- 8 EPIs com lotes variados
- 1 lote vencido e 1 proximo do vencimento
- 10 entregas, 1 devolucao e 1 baixa
- 3 usuarios prontos para uso

## Passo 5 — Acessar o sistema

Abra o navegador em `http://localhost:8000` e faca login com um dos usuarios abaixo:

| Usuario | Senha | Perfil |
|---|---|---|
| `admin` | `admin` | Acesso total, incluindo painel admin |
| `almoxarife` | `almoxarife` | Operacoes: entrega, devolucao e baixa |
| `gestor` | `gestor` | Somente consulta: dashboard e movimentacoes |

## Rotas Disponiveis

| Rota | Descricao | Acesso |
|---|---|---|
| `http://localhost:8000/` | Dashboard | Todos |
| `http://localhost:8000/entregas/nova/` | Registrar entrega | Administrador, Almoxarife |
| `http://localhost:8000/devolucoes/nova/` | Registrar devolucao | Administrador, Almoxarife |
| `http://localhost:8000/baixas/nova/` | Registrar baixa | Administrador, Almoxarife |
| `http://localhost:8000/movimentacoes/` | Historico de movimentacoes | Todos |
| `http://localhost:8000/accounts/login/` | Login | Publico |
| `http://localhost:8000/admin/` | Painel administrativo | Admin |

## Rodar os Testes

```powershell
docker compose exec django python manage.py test
```

## Criar um Superusuario Manualmente

```powershell
docker compose exec django python manage.py createsuperuser
```

## Parar o Ambiente

```powershell
docker compose down
```

Para remover tambem os dados do banco:

```powershell
docker compose down -v
```

## Problemas Comuns

### CSS nao carrega
O Django em modo `runserver` serve arquivos estaticos automaticamente com `DEBUG=True`. Se nao carregar, verifique se o container subiu sem erros.

### Erro de conexao com o banco
O container Django aguarda o banco estar pronto antes de subir. Se o erro persistir, rode:

```powershell
docker compose down
docker compose up --build
```

### Tela de acesso negado ao acessar uma rota
O usuario logado nao tem o grupo necessario. Use `admin` ou `almoxarife` para operacoes, ou acesse o painel admin para atribuir grupos ao usuario.

### Dados duplicados ao rodar o seed novamente
O seed e idempotente: rodar mais de uma vez nao duplica registros ja existentes.
