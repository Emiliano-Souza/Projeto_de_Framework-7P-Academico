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

## Rotina Recomendada de Inicializacao

Para subir o ambiente local e evitar divergencia entre codigo e banco:

```powershell
cd .\Projeto
docker compose up --build
docker compose exec django python manage.py test
```

O `entrypoint.sh` ja executa `migrate` automaticamente ao subir o container. Quando houver migracoes novas, basta reiniciar o container ou rodar manualmente:

```powershell
docker compose exec django python manage.py migrate
```

Se for acessar telas protegidas por login:

```powershell
docker compose exec django python manage.py createsuperuser
```

## Fluxos Web Disponiveis

Com o ambiente rodando e usuario autenticado, as rotas principais atuais sao:

- `http://localhost:8000/entregas/nova/`
- `http://localhost:8000/devolucoes/nova/`
- `http://localhost:8000/baixas/nova/`
- `http://localhost:8000/movimentacoes/`
- `http://localhost:8000/accounts/login/`
- `http://localhost:8000/admin/`

## Healthcheck do Banco
O servico do PostgreSQL possui um `healthcheck` com `pg_isready`.

Esse teste serve para verificar se o banco esta realmente pronto para aceitar conexoes. Isso e util porque um container pode estar iniciado, mas o banco ainda estar em processo interno de subida.

O servico `django` usa `depends_on` com `condition: service_healthy`, garantindo que o container Django so inicia apos o banco estar operacional.

## Observacao Importante
O `healthcheck` com `service_healthy` garante que o Django so sobe quando o banco esta pronto. O `entrypoint.sh` mantem o loop `nc -z` como protecao adicional e exibe logs de cada etapa da inicializacao.

## Diferenca Entre Banco de Teste e Banco Real

Os testes do Django usam um banco temporario criado automaticamente. Por isso:

- testes passando nao significam que o banco real do container ja recebeu as migracoes mais recentes

Quando houver mudanca de model ou migracao nova, o passo `python manage.py migrate` no container real continua obrigatorio.
