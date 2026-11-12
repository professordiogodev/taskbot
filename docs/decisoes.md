# Decisões de desenho

Registo das decisões que explicam o comportamento atual do `taskbot`. Cada
afirmação abaixo pode ser confirmada no código de `src/taskbot/`.

## IDs monotónicos, nunca reutilizados

O identificador de cada tarefa vem do campo `next_id` guardado no ficheiro de
dados (`store.add_task`):

```python
task = Task(id=data["next_id"], text=text, priority=priority)
data["tasks"].append(task.to_dict())
data["next_id"] += 1
```

`next_id` só sobe. `store.remove_task` filtra a lista de tarefas mas **não**
mexe em `next_id`, portanto um ID removido nunca volta a ser atribuído. O
teste `tests/test_store.py::test_ids_never_reused_after_rm` fixa este
comportamento: depois de apagar a tarefa `2`, a tarefa seguinte recebe `3`.

Consequência prática: os IDs não são índices da lista. Numa lista com uma só
tarefa é normal ver `3 [ ] (med) ...`.

## A validação de prioridade vive na CLI

`models.PRIORITIES` é a única fonte de verdade: `("low", "med", "high")`.
`store.add_task` aceita qualquer string como prioridade — quem valida é o
comando `add`, em `cli.py`:

```python
if priority not in PRIORITIES:
    typer.echo(f"Prioridade inválida: {priority}", err=True)
    raise typer.Exit(1)
```

A separação é intencional: o `store` é uma camada de persistência e não impõe
regras de interface. O custo é que uma prioridade inválida escrita à mão no
JSON faria `list` falhar em `_ORDER[t.priority]` (`KeyError`), porque
`_ORDER` só tem chaves para as três prioridades conhecidas.

## Ordenação: `high` primeiro, empate pelo ID

`cli.py` define a ordem a partir de `PRIORITIES`, invertendo a tupla:

```python
_ORDER = {p: i for i, p in enumerate(reversed(PRIORITIES))}
```

O resultado é `high = 0`, `med = 1`, `low = 2`. `list` ordena com
`key=lambda t: (_ORDER[t.priority], t.id)`, ou seja prioridade primeiro e, em
caso de empate, ID crescente (mais antiga primeiro). Tarefas concluídas
**não** são escondidas nem despriorizadas — continuam na lista, apenas com
`[x]`.

## Leitura tolerante, escrita normalizada

`store._load` trata o ficheiro com tolerância para não quebrar dados antigos:

- ficheiro inexistente → `{"next_id": 1, "tasks": []}`;
- sem `next_id` → `max(id) + 1` (ou `1` se não houver tarefas);
- `Task.from_dict` usa `data.get("done", False)` e
  `data.get("priority", "med")`, pelo que tarefas sem esses campos são lidas
  com os valores por omissão.

`_load` devolve sempre um dicionário com **apenas** `next_id` e `tasks`. Como
`_save` escreve exatamente esse dicionário, quaisquer chaves extra no topo do
JSON são descartadas na primeira escrita seguinte. É o preço aceite por manter
o formato pequeno e previsível.

## JSON legível em vez de formato binário

`store._save` grava com:

```python
path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
```

`indent=2` e `ensure_ascii=False` tornam o ficheiro legível e os acentos
preservados (`"estudar programação"` fica literal, não `\u00e7`). A escolha
permite inspecionar e editar o ficheiro à mão, e é a razão pela qual não há
base de dados nem migrações: o formato é o contrato descrito em
[`formato-ficheiro.md`](formato-ficheiro.md).
