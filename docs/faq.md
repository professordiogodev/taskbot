# FAQ

Perguntas frequentes sobre o `taskbot`, com respostas verificáveis em
`src/taskbot/`.

## Onde é que as tarefas ficam guardadas?

Num único ficheiro JSON, `~/.taskbot.json` por omissão. O caminho é decidido
por `store.default_path()`:

```python
return Path(os.environ.get("TASKBOT_FILE", Path.home() / ".taskbot.json"))
```

Se definires a variável de ambiente `TASKBOT_FILE`, o `taskbot` passa a usar
esse caminho em vez do ficheiro na home. É útil para teres listas separadas
(por projeto, por contexto) sem qualquer flag na CLI:

```console
$ TASKBOT_FILE=./trabalho.json taskbot add "revisão de código"
Tarefa 1 criada.
```

O ficheiro é criado na primeira escrita; antes disso não existe. `list` sobre
um ficheiro inexistente devolve uma lista vazia sem erro, porque `_load`
devolve `{"next_id": 1, "tasks": []}`.

## Porque é que o primeiro ID é 1 e depois salta números?

Os IDs vêm de `next_id`, que só aumenta e nunca é recalculado a partir da
lista. `store.remove_task` remove a tarefa mas não toca em `next_id`, por
isso um ID apagado não volta a aparecer. Ver
`tests/test_store.py::test_ids_never_reused_after_rm`:

```python
store.add_task("a", path=path)     # id 1
store.add_task("b", path=path)     # id 2
store.remove_task(2, path=path)
assert store.add_task("c", path=path).id == 3
```

Saltos na numeração são portanto esperados, não um bug.

## Porque é que `done 7` diz que a tarefa não existe?

Porque não há nenhuma tarefa com `id == 7`. `store.mark_done` percorre as
tarefas e, se não encontrar o ID, levanta `KeyError`; a CLI traduz isso em:

```console
$ taskbot done 7
Tarefa 7 não existe.
$ echo $?
1
```

O mesmo acontece com `rm 7` e com a mesma mensagem e código de saída. O
comando `list` mostra os IDs válidos na primeira coluna — nota que o ID não é
a posição na lista.

## Como é que sei a prioridade de uma tarefa?

A prioridade aparece entre parênteses na listagem, e a ordem já a revela:
`high` primeiro, depois `med`, depois `low`. Os únicos valores válidos são
`low`, `med` e `high` (`models.PRIORITIES`), e o valor por omissão é `med`:

```console
$ taskbot add "sem prioridade"
Tarefa 1 criada.
$ taskbot list
1 [ ] (med) sem prioridade
$ taskbot add "urgente" -p high
Tarefa 2 criada.
$ taskbot list
2 [ ] (high) urgente
1 [ ] (med) sem prioridade
```

Uma prioridade inventada é recusada antes de escrever no ficheiro:
`taskbot add "a" -p x` imprime `Prioridade inválida: x` e sai com código `1`.

## Posso editar o ficheiro JSON à mão?

Podes — é JSON indentado com dois espaços e UTF-8, sem escapes para acentos.
Duas regras para não quebrares o estado:

- mantém `next_id` **maior** que todos os `id` existentes; se o campo faltar,
  o `taskbot` calcula `max(id) + 1`, mas se estiver presente confia no valor
  gravado e pode reutilizar IDs;
- usa só `low`, `med` ou `high` em `priority`; qualquer outro valor faz
  `list` rebentar com `KeyError` ao indexar `_ORDER`.

Os detalhes do formato estão em [`formato-ficheiro.md`](formato-ficheiro.md).

## Como começo do zero?

Apaga o ficheiro de dados:

```console
$ rm ~/.taskbot.json
$ taskbot list      # saída vazia
$ taskbot add "primeira"
Tarefa 1 criada.
```

Se usas `TASKBOT_FILE`, apaga o ficheiro para onde essa variável aponta. Não
há mais estado em lado nenhum: o `taskbot` não usa base de dados nem cache.
