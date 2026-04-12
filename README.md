# Sistema Web de Gestao de Entrega de EPIs

## Descricao do Projeto
Este sistema foi desenvolvido para automatizar o controle e gerenciamento de Equipamentos de Protecao Individual (EPIs). A solucao permite o cadastro de funcionarios e equipamentos, controle de estoque em tempo real, monitoramento de validades e o registro historico de entregas, devolucoes e baixas.

## Framework e Tecnologias
O projeto foi desenvolvido com **Django (Python)**, utilizando:

- ORM nativo do Django para modelagem e integridade
- PostgreSQL como banco relacional
- Docker Compose para ambiente local
- sistema de autenticacao nativo do Django
- admin nativo do Django para apoio operacional
- suite de testes automatizados para validar regras do dominio

## Documentacao
A documentacao tecnica do projeto esta organizada na pasta `docs/`.

- `docs/como_rodar.md`: tutorial completo para subir o projeto do zero
- `docs/arquitetura.md`: visao da arquitetura, containers e organizacao do sistema
- `docs/configuracao_ambiente.md`: como o ambiente local funciona
- `docs/banco_de_dados.md`: modelagem do banco, decisoes e evolucao das tabelas
- `docs/regras_de_negocio.md`: regras funcionais e principios de integridade
- `docs/testes.md`: estrategia de testes, cobertura atual e como executar
- `docs/estrutura_django.md`: organizacao do projeto dentro do Django
- `docs/fluxos_aplicacao.md`: fluxos tecnicos de entrega, devolucao e baixa
- `docs/guia_tecnico.md`: particularidades do codigo, snippets e pontos de manutencao
- `docs/anatomia_service_entregas.md`: explicacao detalhada do arquivo central de regras operacionais
- `docs/decisoes_tecnicas.md`: justificativas das escolhas tecnicas
- `docs/historico_do_projeto.md`: evolucao do projeto por etapas

## Estado Atual
Neste momento, o projeto possui:

- estrutura base em Django organizada por app
- PostgreSQL em container separado via Docker Compose
- modelagem principal do banco implementada
- fluxos web iniciais de entrega, devolucao e baixa
- tela de historico de movimentacoes do estoque
- camada de service para regras operacionais
- autenticacao basica
- testes automatizados rodando no Docker
- documentacao funcional e tecnica

## Rotina de Desenvolvimento
Comandos mais usados no projeto:

```powershell
cd .\Projeto
docker compose up --build
docker compose exec django python manage.py migrate
docker compose exec django python manage.py test
docker compose exec django python manage.py createsuperuser
```

## Autores
* **Emiliano Ferreira de Souza Junior**
* **Mario Alves Fernandes Neto**

---
*Projeto academico desenvolvido para o curso de Sistemas de Informacao.*
