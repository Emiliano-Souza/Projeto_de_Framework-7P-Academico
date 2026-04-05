# Anatomia do Service `entregas.py`

## Objetivo
Este documento explica, funcao por funcao, como o arquivo `Projeto/epi/services/entregas.py` foi desenhado e qual o papel de cada bloco no fluxo do sistema.

## Papel do Arquivo
`services/entregas.py` eh hoje o centro da regra operacional do projeto.

Ele concentra tres casos de uso principais:

- entrega
- devolucao
- baixa

E uma funcao transversal:

- persistencia operacional de `EntregaEPI`

Em termos práticos, ele faz a ponte entre:

- regras do dominio
- consistencia de estoque
- criacao de movimentacoes
- transacao e controle de concorrencia

## Visao Geral das Funcoes

Ordem atual do arquivo:

1. `_validar_funcionario_ativo`
2. `_ajustar_status_e_campos_de_devolucao`
3. `_saldo_aberto_da_entrega`
4. `_validar_reducao_retroativa`
5. `persistir_entrega_epi`
6. `_validar_lote_disponivel_para_entrega`
7. `registrar_entrega_epi`
8. `registrar_devolucao_epi`
9. `registrar_baixa_epi`

Essa ordem nao eh acidental.

Ela segue uma progressao natural:

- helpers pequenos
- helper central de persistencia
- casos de uso publicos

## 1. `_validar_funcionario_ativo`

### Funcao
Valida se o funcionario selecionado para entrega ainda esta ativo.

Trecho:

```python
def _validar_funcionario_ativo(funcionario):
    if not funcionario.ativo:
        raise ValidationError({"funcionario": "O funcionario selecionado esta inativo."})
```

### Por que existe
Essa regra depende do contexto da operacao, nao apenas da estrutura do banco.

Ela faz sentido no service porque:

- eh regra operacional
- precisa ser reaproveitada
- nao deve ficar escondida na view

### Observacao tecnica
O erro ja vem estruturado por campo (`funcionario`), o que facilita acoplamento com `form.add_error(...)`.

## 2. `_ajustar_status_e_campos_de_devolucao`

### Funcao
Sincroniza os campos relacionados a devolucao:

- `usuario_devolucao`
- `data_devolucao`
- `status`

Trecho conceitual:

```python
if entrega.quantidade_devolvida > 0:
    ...
else:
    entrega.data_devolucao = None
    entrega.usuario_devolucao = None
```

### O que ela decide

- se existe devolucao, deve haver usuario
- se existe devolucao e a data nao foi informada, a data atual e atribuida
- se nao existe devolucao, os campos de devolucao sao limpos
- o status eh recalculado com base na quantidade devolvida

### Por que isso nao ficou no form
Porque essa logica vale tanto para:

- fluxo web
- admin
- ORM direto
- service

Ou seja, ela pertence ao dominio, nao apenas a interface.

### Limite atual
O status ainda nao modela todos os estados possiveis de uma entrega com baixa parcial, por escolha de simplicidade.

## 3. `_saldo_aberto_da_entrega`

### Funcao
Calcula quanto ainda resta "aberto" em uma entrega:

```python
quantidade_entregue - quantidade_devolvida - quantidade_baixada
```

### Por que isso importa
Esse valor eh a base para:

- devolucao futura
- baixa futura
- validacoes de encerramento

### Por que virou helper
Porque esse calculo tende a reaparecer e faz sentido ter uma fonte unica para a regra.

## 4. `_validar_reducao_retroativa`

### Funcao
Impede que quantidades ja registradas sejam reduzidas depois:

- `quantidade_entregue`
- `quantidade_devolvida`
- `quantidade_baixada`

### Ideia
O sistema permite aumentar efeitos acumulados coerentes, mas nao "apagar historico" retroativamente.

Trecho conceitual:

```python
if entrega.quantidade_devolvida < entrega_anterior.quantidade_devolvida:
    errors["quantidade_devolvida"] = ...
```

### Por que isso eh importante
Sem essa validacao, alguem poderia:

- devolver 3
- depois mudar para 1
- quebrar a coerencia entre entrega, lote e historico

### Observacao tecnica
Essa funcao usa o estado anterior do banco como referencia de verdade operacional.

## 5. `persistir_entrega_epi`

### Funcao
Eh a funcao mais importante do arquivo.

Ela resolve toda a persistencia operacional de `EntregaEPI`.

### Responsabilidades

- abrir transacao
- travar lote
- recuperar estado anterior da entrega
- ajustar campos de devolucao/status
- validar reducao retroativa
- executar `full_clean`
- calcular deltas
- recalcular saldo do lote
- salvar lote
- salvar entrega
- criar movimentacoes

### Etapa 1: transacao e lock

Trecho:

```python
with transaction.atomic():
    lote = EPILote.objects.select_for_update().get(pk=entrega.epi_lote_id)
```

### O que isso garante

- as alteracoes acontecem como unidade atomica
- duas operacoes concorrentes no mesmo lote nao seguem cegamente em paralelo

### Etapa 2: carregar entrega anterior

Trecho:

```python
if entrega.pk:
    entrega_anterior = (
        EntregaEPI.objects.select_for_update()
        .filter(pk=entrega.pk)
        .first()
    )
```

### Por que isso existe
Sem o estado anterior, nao seria possivel calcular:

- o quanto foi entregue agora
- o quanto foi devolvido agora
- o quanto foi baixado agora

### Etapa 3: validacoes e normalizacao

Trecho:

```python
_ajustar_status_e_campos_de_devolucao(entrega)
_validar_reducao_retroativa(entrega, entrega_anterior)
entrega.full_clean()
```

### Por que a ordem importa

1. primeiro a instancia e normalizada
2. depois se protege contra reducao retroativa
3. depois o Django valida constraints de model

Se `full_clean()` viesse antes, alguns campos ajustados na propria funcao ainda nao estariam coerentes.

### Etapa 4: deltas

Trecho:

```python
delta_entrega = entrega.quantidade_entregue - quantidade_entregue_anterior
delta_devolucao = entrega.quantidade_devolvida - quantidade_devolvida_anterior
delta_baixa = entrega.quantidade_baixada - quantidade_baixada_anterior
```

### Leitura conceitual

- `delta_entrega`: quanto saiu do lote agora
- `delta_devolucao`: quanto voltou ao lote agora
- `delta_baixa`: quanto foi encerrado agora sem retorno ao lote

### Etapa 5: recalculo do lote

Trecho:

```python
novo_saldo = lote.quantidade_disponivel - delta_entrega + delta_devolucao
```

### Detalhe importante
`delta_baixa` nao entra nessa conta.

Motivo:

- baixa nao devolve item ao lote
- baixa tambem nao consome saldo novo do lote
- o lote ja foi impactado no momento da entrega

### Etapa 6: salvar lote

Trecho:

```python
lote.quantidade_disponivel = novo_saldo
lote.save(update_fields=["quantidade_disponivel", "updated_at"])
```

### Por que `update_fields`
Porque a alteracao eh pequena e intencional. Isso reduz efeitos colaterais e deixa a operacao mais explicita.

### Etapa 7: salvar entrega

Trecho:

```python
super(EntregaEPI, entrega).save(*args, **kwargs)
```

### Esse eh um detalhe critico
O uso de `super(EntregaEPI, entrega).save(...)` evita chamar de novo o `save()` sobrescrito do model.

Se chamasse `entrega.save()` aqui, haveria recursao.

### Etapa 8: criar movimentacoes

O arquivo cria ate tres tipos de movimentacao:

- `ENTREGA`
- `DEVOLUCAO`
- `BAIXA`

Cada uma depende do delta correspondente ser maior que zero.

### Particularidade da baixa

Trecho conceitual:

```python
quantidade_antes=saldo_cursor,
quantidade_depois=saldo_cursor,
```

Isso documenta:

- houve evento de dominio
- nao houve retorno nem novo consumo no lote

## 6. `_validar_lote_disponivel_para_entrega`

### Funcao
Valida a operacao de entrega em relacao ao lote:

- lote nao vencido
- saldo suficiente

### Por que ela nao participa de devolucao/baixa
Porque devolucao e baixa partem de `EntregaEPI`, nao de um lote solto selecionado pelo usuario.

## 7. `registrar_entrega_epi`

### Funcao
Caso de uso publico para criar uma entrega.

### O que ela faz

1. define data se nao vier
2. valida funcionario ativo
3. valida lote
4. monta a instancia `EntregaEPI`
5. delega para `persistir_entrega_epi`

### Por que nao faz tudo direto na view
Para manter:

- view simples
- regra reutilizavel
- testes mais faceis

## 8. `registrar_devolucao_epi`

### Funcao
Caso de uso publico para devolver parte de uma entrega existente.

### O que ela valida

- quantidade positiva
- entrega existente
- saldo pendente suficiente

### O que ela altera

- incrementa `quantidade_devolvida`
- define `usuario_devolucao`
- define `data_devolucao`
- opcionalmente atualiza observacao

### Observacao
Ela nao mexe no lote diretamente. Quem faz isso e a persistencia central.

## 9. `registrar_baixa_epi`

### Funcao
Caso de uso publico para encerrar quantidade entregue sem retorno ao estoque.

### O que ela valida

- quantidade positiva
- motivo obrigatorio
- entrega existente
- saldo em aberto suficiente

### O que ela altera

- incrementa `quantidade_baixada`
- registra usuario responsavel
- prefixa a observacao com o motivo

### Observacao tecnica
Hoje ela reutiliza `usuario_devolucao` para guardar o usuario da baixa.

Isso funciona, mas ainda nao eh o desenho ideal. Futuramente pode virar um campo proprio.

## 10. Decisoes Arquiteturais Importantes

### 1. Um unico service para tres operacoes
Foi escolhido porque os tres fluxos giram em torno de `EntregaEPI` e compartilham persistencia comum.

### 2. Uma unica funcao central de persistencia
Foi escolhida para evitar divergencia entre:

- entrega
- devolucao
- baixa

### 3. Mistura controlada entre model e service
O projeto nao esta totalmente em domain services nem totalmente em fat models. O desenho atual tenta equilibrar:

- compatibilidade com Django
- clareza de regra
- baixo atrito de manutencao

## 11. O Que Observar ao Refatorar Esse Arquivo

Se for mexer nele no futuro, conferir sempre:

- se `full_clean()` ainda roda na ordem correta
- se `select_for_update()` continua protegendo o lote
- se os deltas continuam consistentes
- se a baixa continua sem alterar o lote
- se a movimentacao criada corresponde exatamente ao delta calculado
- se testes de dominio e de view continuam passando

## 12. Leitura Recomendada Junto com Este Documento

- `Projeto/epi/models.py`
- `Projeto/epi/tests/test_entrada_saida.py`
- `docs/fluxos_aplicacao.md`
- `docs/guia_tecnico.md`
