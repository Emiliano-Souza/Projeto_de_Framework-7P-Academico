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
