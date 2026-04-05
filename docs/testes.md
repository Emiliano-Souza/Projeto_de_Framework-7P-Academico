# Testes

## Objetivo
Este documento descreve a estrategia de testes automatizados do projeto, a organizacao atual da suite e o que ja esta coberto na camada de banco e regra de negocio.

## Papel dos Testes Neste Projeto
Os testes atuais foram criados para validar o nucleo do sistema:

- integridade dos dados
- consistencia do estoque
- rastreabilidade das operacoes
- comportamento das regras de entrega e devolucao

Mais do que verificar se o sistema "roda", os testes demonstram que as regras mais importantes do dominio estao funcionando de forma previsivel.

## Estrutura Atual da Suite
Os testes do dominio `epi` foram organizados em:

- `Projeto/epi/tests/base.py`
- `Projeto/epi/tests/test_cadastros.py`
- `Projeto/epi/tests/test_lotes.py`
- `Projeto/epi/tests/test_entrada_saida.py`
- `Projeto/epi/tests/test_movimentacoes.py`

Essa divisao melhora a leitura e facilita manutencao, porque cada arquivo concentra um grupo coerente de responsabilidades.

## Base Compartilhada
O arquivo `base.py` centraliza os objetos comuns usados nos testes:

- usuario do Django
- setor
- funcionario
- EPI
- lote inicial

Isso reduz repeticao e torna a suite mais consistente.

## Cobertura Atual

### 1. Cadastros e integridade estrutural
Cobertura atual:

- unicidade de `setor.nome`
- unicidade de `funcionario.matricula`
- unicidade de `epi.codigo_interno`
- comportamento de `PROTECT` em exclusoes sensiveis

### 2. Lotes de estoque
Cobertura atual:

- lote nao pode ter saldo maior que quantidade recebida
- lote nao pode repetir `numero_lote` para o mesmo EPI
- lote nao pode ter quantidade recebida invalida

### 3. Entregas e devolucoes
Cobertura atual:

- entrega baixa o saldo do lote
- entrega gera movimentacao
- devolucao devolve saldo ao lote
- devolucao gera movimentacao
- status muda automaticamente conforme o nivel de devolucao
- entrega acima do saldo e bloqueada
- reducoes retroativas de quantidade sao bloqueadas
- devolucao invalida e bloqueada
- multiplas entregas no mesmo lote consomem saldo acumuladamente
- devolucao total restaura o saldo do lote

### 4. Movimentacoes de estoque
Cobertura atual:

- movimentacao com quantidade zero e invalida
- movimentacao com saldo final negativo e invalida

## Como Executar os Testes
No ambiente atual do projeto, os testes foram executados com Docker:

```powershell
docker compose exec django python manage.py test
```

## Resultado Atual
A suite atual possui 20 testes automatizados e todos passaram na validacao mais recente executada dentro do container Django.

## O Que os Testes Ja Garantem
Os testes ja garantem que:

- a modelagem principal do banco esta coerente
- as regras mais sensiveis do estoque estao protegidas
- a entrega e a devolucao alteram o saldo de forma consistente
- a rastreabilidade por movimentacao esta funcionando
- relacionamentos protegidos nao permitem exclusoes indevidas

## O Que Ainda Pode Ser Testado no Futuro
Melhorias possiveis para a suite:

- testes especificos para criacao automatica de movimentacao de entrada
- testes de concorrencia e cenarios mais avancados de transacao
- testes do admin
- testes de integracao de fluxos completos
- testes de interface, quando a camada web for evoluida

## Conclusao
A suite atual ja oferece uma boa confianca sobre o coracao da modelagem e das regras operacionais do sistema. Para o estagio atual do projeto, ela esta bem alinhada com os riscos mais importantes da aplicacao.
