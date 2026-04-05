# Fluxos da Aplicacao

## Objetivo
Este documento descreve como os principais fluxos do sistema funcionam do ponto de vista tecnico: entrega, devolucao e baixa.

## Visao Geral
Os tres fluxos seguem o mesmo desenho:

1. usuario acessa a tela
2. a view valida autenticacao
3. o formulario filtra as opcoes validas
4. o service aplica as regras de negocio
5. o model e persistido
6. a movimentacao de estoque e registrada

## Fluxo de Entrega

### Passo a passo

1. o usuario acessa `/entregas/nova/`
2. a view `registrar_entrega_view` instancia `EntregaEPIForm`
3. o form mostra apenas:
- funcionarios ativos
- lotes com saldo disponivel
4. no POST, a view chama `registrar_entrega_epi(...)`
5. o service valida:
- funcionario ativo
- lote nao vencido
- saldo suficiente
6. a persistencia central reduz o lote
7. o sistema cria `MovimentacaoEstoque` do tipo `ENTREGA`
8. a view exibe mensagem de sucesso

### Trecho central

```python
registrar_entrega_epi(
    funcionario=form.cleaned_data["funcionario"],
    epi_lote=form.cleaned_data["epi_lote"],
    quantidade_entregue=form.cleaned_data["quantidade_entregue"],
    usuario_entrega=request.user,
    data_entrega=form.cleaned_data["data_entrega"],
    confirmado_recebimento=form.cleaned_data["confirmado_recebimento"],
    observacao=form.cleaned_data["observacao"],
)
```

## Fluxo de Devolucao

### Passo a passo

1. o usuario acessa `/devolucoes/nova/`
2. a view `registrar_devolucao_view` instancia `DevolucaoEPIForm`
3. o form mostra apenas entregas com devolucao pendente
4. no POST, a view chama `registrar_devolucao_epi(...)`
5. o service valida:
- entrega existente
- quantidade positiva
- saldo pendente suficiente
6. a persistencia central aumenta `quantidade_devolvida`
7. o lote recebe saldo de volta
8. o sistema cria `MovimentacaoEstoque` do tipo `DEVOLUCAO`
9. a view exibe mensagem de sucesso

### Trecho central

```python
registrar_devolucao_epi(
    entrega_id=form.cleaned_data["entrega"].pk,
    quantidade_devolvida=form.cleaned_data["quantidade_devolvida"],
    usuario_devolucao=request.user,
    observacao=form.cleaned_data["observacao"],
)
```

## Fluxo de Baixa

### Ideia
Baixa representa encerramento de quantidade entregue sem retorno ao estoque.

Casos comuns:

- extraviado
- danificado
- vencido
- descartado

### Passo a passo

1. o usuario acessa `/baixas/nova/`
2. a view `registrar_baixa_view` instancia `BaixaEPIForm`
3. o form mostra apenas entregas com saldo em aberto
4. no POST, a view chama `registrar_baixa_epi(...)`
5. o service valida:
- entrega existente
- quantidade positiva
- motivo obrigatorio
- saldo em aberto suficiente
6. a persistencia central aumenta `quantidade_baixada`
7. o lote nao recebe saldo de volta
8. o sistema cria `MovimentacaoEstoque` do tipo `BAIXA`
9. a view exibe mensagem de sucesso

### Trecho central

```python
registrar_baixa_epi(
    entrega_id=form.cleaned_data["entrega"].pk,
    quantidade_baixada=form.cleaned_data["quantidade_baixada"],
    usuario_baixa=request.user,
    motivo_baixa=form.cleaned_data["motivo_baixa"],
    observacao=form.cleaned_data["observacao"],
)
```

## Persistencia Central

O ponto tecnico mais importante do projeto eh `persistir_entrega_epi(...)`.

Essa funcao resolve:

- transacao
- leitura com lock do lote
- deltas de entrega, devolucao e baixa
- ajuste de saldo do lote
- criacao das movimentacoes

Trecho relevante:

```python
delta_entrega = entrega.quantidade_entregue - quantidade_entregue_anterior
delta_devolucao = entrega.quantidade_devolvida - quantidade_devolvida_anterior
delta_baixa = entrega.quantidade_baixada - quantidade_baixada_anterior
novo_saldo = lote.quantidade_disponivel - delta_entrega + delta_devolucao
```

Interpretacao:

- entrega reduz lote
- devolucao devolve saldo ao lote
- baixa nao altera o lote

## Por Que a Baixa Nao Muda o Lote
O lote ja foi reduzido no momento da entrega.

Quando a baixa acontece, ela apenas encerra a parte ainda aberta daquela entrega. Por isso a movimentacao de baixa e registrada com:

- `quantidade_antes == quantidade_depois`

Isso mostra que:

- houve evento operacional
- nao houve retorno fisico ao estoque

## Regras Criticas

### Entrega
- nao entregar acima do saldo do lote
- nao entregar lote vencido
- nao entregar para funcionario inativo

### Devolucao
- nao devolver acima do saldo pendente
- nao devolver quantidade zero ou negativa
- nao devolver entrega inexistente

### Baixa
- nao baixar acima do saldo em aberto
- nao baixar quantidade zero ou negativa
- nao baixar sem motivo
- nao usar baixa para aumentar estoque

## Onde Ler no Codigo

- `Projeto/epi/forms.py`
- `Projeto/epi/views/entregas.py`
- `Projeto/epi/views/devolucoes.py`
- `Projeto/epi/views/baixas.py`
- `Projeto/epi/services/entregas.py`
- `Projeto/epi/tests/test_entrada_saida.py`
- `Projeto/epi/tests/test_views.py`
