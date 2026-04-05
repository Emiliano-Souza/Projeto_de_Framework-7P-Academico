# Guia Tecnico

## Objetivo
Este documento destaca trechos importantes do codigo e explica particularidades do projeto para quem vai manter ou evoluir a aplicacao.

## 1. Por Que Existe uma Camada de Service

O projeto comecou com forte foco em modelagem e integridade. Conforme os fluxos cresceram, foi introduzida uma camada de service para deixar a regra de negocio mais explicita.

Hoje ela centraliza:

- entrega
- devolucao
- baixa
- persistencia operacional

Trecho relevante:

```python
def registrar_entrega_epi(...):
    _validar_funcionario_ativo(funcionario)
    _validar_lote_disponivel_para_entrega(...)

    entrega = EntregaEPI(...)
    return persistir_entrega_epi(entrega)
```

Beneficio:

- a view continua simples
- a regra fica testavel
- a manutencao nao depende de procurar logica espalhada

## 2. Por Que o Model Ainda Sobrescreve `save()`

Mesmo com a camada de service, `EntregaEPI.save()` nao foi abandonado. Ele delega para o service:

```python
def save(self, *args, **kwargs):
    from epi.services.entregas import persistir_entrega_epi
    return persistir_entrega_epi(self, *args, **kwargs)
```

Isso foi mantido por tres motivos:

- preserva consistencia quando o objeto e salvo via ORM
- evita comportamento divergente no admin do Django
- reduz risco de alguem contornar a regra operacional sem perceber

## 3. O Ponto Mais Sensivel: `persistir_entrega_epi`

Essa funcao eh o coracao do dominio atual.

Ela:

- abre transacao
- trava o lote com `select_for_update`
- calcula diferencas entre estado anterior e novo
- aplica alteracao de saldo
- cria movimentacoes

Trecho relevante:

```python
with transaction.atomic():
    lote = EPILote.objects.select_for_update().get(pk=entrega.epi_lote_id)
```

Por que isso importa:

- evita inconsistencias em operacoes concorrentes
- garante que lote e entrega sejam atualizados juntos

## 4. Deltas em vez de Regra Duplicada

O projeto nao grava "saldo final" diretamente dentro da entrega. Em vez disso, compara o estado anterior com o novo estado do registro:

```python
delta_entrega = entrega.quantidade_entregue - quantidade_entregue_anterior
delta_devolucao = entrega.quantidade_devolvida - quantidade_devolvida_anterior
delta_baixa = entrega.quantidade_baixada - quantidade_baixada_anterior
```

Essa estrategia permite:

- criacao de entrega nova
- atualizacao por devolucao
- atualizacao por baixa

sem duplicar fluxos separados de persistencia.

## 5. Particularidade do Django: testes podem passar e o banco real ainda estar atrasado

Os testes do Django criam um banco temporario e aplicam as migracoes nele. Isso significa:

- teste passando nao garante que o banco real do container esteja atualizado

Exemplo real do projeto:

- o codigo passou a usar `quantidade_baixada`
- os testes passaram
- a tela web que usa o banco real falhou ate rodarmos `migrate`

Rotina correta quando houver mudanca de banco:

1. alterar model
2. criar migracao
3. rodar testes
4. rodar `migrate` no banco real
5. testar na interface

## 6. Particularidade do Django: `login_required` depende de URL de autenticacao

As views web usam `@login_required`. Isso exige que a rota de login exista:

```python
path("accounts/", include("django.contrib.auth.urls"))
```

Sem isso, o Django redireciona para `/accounts/login/`, mas a pagina nao existe.

## 7. Querysets filtrados nos forms

Os formularios nao servem apenas para renderizar campos. Eles tambem ajudam a prevenir operacoes invalidas antes mesmo do POST:

```python
self.fields["epi_lote"].queryset = EPILote.objects.filter(
    quantidade_disponivel__gt=0
).order_by("data_validade", "numero_lote")
```

E:

```python
self.fields["entrega"].queryset = (
    EntregaEPI.objects.select_related("funcionario", "epi_lote", "epi_lote__epi")
    .filter(quantidade_devolvida__lt=(F("quantidade_entregue") - F("quantidade_baixada")))
)
```

Beneficios:

- menos erro operacional
- menos chance de submit invalido
- interface mais coerente com as regras

## 8. Por Que `PROTECT` Foi Escolhido

O projeto usa `on_delete=PROTECT` em entidades historicas porque excluir registros centrais poderia corromper o historico operacional.

Exemplos:

- nao apagar `setor` ligado a funcionario
- nao apagar `funcionario` ligado a entrega
- nao apagar `epi_lote` ligado a entrega ou movimentacao

## 9. Diferenca Entre Devolucao e Baixa

Essa eh uma regra importante do dominio:

- devolucao aumenta o saldo do lote
- baixa nao aumenta o saldo do lote

Em termos tecnicos:

```python
novo_saldo = lote.quantidade_disponivel - delta_entrega + delta_devolucao
```

Repare que `delta_baixa` nao participa da conta do lote.

Isso foi intencional.

## 10. Como Ler os Testes

Os testes foram organizados para refletir riscos do projeto:

- `test_forms.py`: filtros e validacao de formularios
- `test_views.py`: autenticacao, renderizacao e submissao web
- `test_entrada_saida.py`: regras centrais do dominio
- `test_movimentacoes.py`: integridade da auditoria

Leitura recomendada:

1. `test_entrada_saida.py`
2. `services/entregas.py`
3. `views/`
4. `forms.py`

## 11. Comandos Tecnicos Mais Usados

### Rodar testes

```powershell
docker compose exec django python manage.py test
```

### Aplicar migracoes

```powershell
docker compose exec django python manage.py migrate
```

### Criar superusuario

```powershell
docker compose exec django python manage.py createsuperuser
```

### Subir ambiente

```powershell
docker compose up --build
```

## 12. Pontos que Ainda Merecem Evolucao

- separar melhor usuario de devolucao e usuario de baixa
- tratar estados mais sofisticados da entrega
- adicionar listagens e dashboards
- melhorar navegacao entre fluxos
- ampliar documentacao de deploy

## Resumo
Para um dev, os pontos mais importantes do projeto hoje sao:

- a regra central esta em `services/entregas.py`
- `EntregaEPI` eh a entidade operacional principal
- testes e migracoes precisam ser tratados juntos
- as tres operacoes principais do dominio ja existem: entrega, devolucao e baixa
