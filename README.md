# Sistema Web de Gestão de Entrega de EPIs

## 📝 Descrição do Projeto
Este sistema foi desenvolvido para automatizar o controle e gerenciamento de Equipamentos de Proteção Individual (EPIs). A solução permite o cadastro de funcionários e equipamentos, controle de estoque em tempo real, monitoramento de validades e o registro histórico de entregas, eliminando falhas de processos manuais e garantindo a segurança no ambiente de trabalho.

## 🛠️ Framework e Tecnologias
O projeto foi desenvolvido utilizando o framework **Django (Python)**, aproveitando sua estrutura robusta de ORM e o sistema de administração nativo para garantir a integridade dos dados e a agilidade no gerenciamento das informações de segurança do trabalho.

## 📚 Documentação
A documentação técnica do projeto está organizada na pasta `docs/`.

- `docs/arquitetura.md`: visão da arquitetura, containers e organização do sistema
- `docs/configuracao_ambiente.md`: como o ambiente local funciona
- `docs/banco_de_dados.md`: modelagem do banco, decisões e evolução das tabelas
- `docs/regras_de_negocio.md`: regras funcionais e princípios de integridade
- `docs/testes.md`: estratégia de testes, cobertura atual e como executar
- `docs/decisoes_tecnicas.md`: justificativas das escolhas técnicas
- `docs/historico_do_projeto.md`: evolução do projeto por etapas

## 🚧 Estado Atual
Neste momento, o projeto possui:

- estrutura base em Django
- PostgreSQL em container separado via Docker Compose
- app de domínio inicial para a gestão de EPIs
- primeira tabela do banco implementada: `setor`

## 👥 Autores
* **Emiliano Ferreira de Souza Junior**
* **Mário Alves Fernandes Neto**

---
*Projeto acadêmico desenvolvido para o curso de Sistemas de Informação.*
