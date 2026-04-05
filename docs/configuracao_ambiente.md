# Configuracao do Ambiente

## Stack Atual

- Python 3.12
- Django 5.2
- PostgreSQL 16
- Docker e Docker Compose

## Containers
O ambiente local foi estruturado com dois containers:

- `epi_db`: container do PostgreSQL
- `epi_django`: container da aplicacao Django

## Portas

- aplicacao Django: `8000`
- PostgreSQL externo: `55432`
- PostgreSQL interno na rede Docker: `5432`

## Variaveis de Ambiente
O projeto utiliza um arquivo `.env` para configurar o banco. As variaveis esperadas atualmente sao:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DB_HOST`
- `DB_PORT`

No uso padrao com Docker Compose:

- `DB_HOST=db`
- `DB_PORT=5432`

## Healthcheck do Banco
O servico do PostgreSQL possui um `healthcheck` com `pg_isready`.

Esse teste serve para verificar se o banco esta realmente pronto para aceitar conexoes. Isso e util porque um container pode estar iniciado, mas o banco ainda estar em processo interno de subida.

## Observacao Importante
O `healthcheck` melhora a observabilidade do servico, mas a protecao pratica principal do ambiente ainda esta no `entrypoint.sh`, que espera o banco responder antes de iniciar o Django.
