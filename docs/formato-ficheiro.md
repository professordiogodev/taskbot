# Formato do ficheiro de dados

O `taskbot` guarda tudo num único ficheiro JSON. Este documento descreve o
formato tal como é produzido por `src/taskbot/store.py`.

## Localização do ficheiro

O caminho é resolvido por `store.default_path()`:

```python
def default_path() -> Path:
    return Path(os.environ.get("TASKBOT_FILE", Path.home() / ".taskbot.json"))
```

- por omissão: `~/.taskbot.json`;
- se a variável de ambiente `TASKBOT_FILE` estiver definida, o seu valor
  substitui o caminho por omissão.

Os testes usam precisamente essa variável: o fixture `taskfile` em
`tests/test_cli.py` faz `monkeypatch.setenv("TASKBOT_FILE", ...)` para apontar
a um ficheiro temporário e não tocar no `~/.taskbot.json` real.

## Estrutura do documento

O ficheiro tem dois campos de topo — `next_id` e `tasks` — e cada tarefa tem
quatro campos:

```json
{
  "next_id": 3,
  "tasks": [
    {
      "id": 1,
      "text": "tarefa longa",
      "done": false,
      "priority": "high"
    },
    {
      "id": 2,
      "text": "b",
      "done": false,
      "priority": "med"
    }
  ]
}
```

| Campo | Tipo | Origem |
| --- | --- | --- |
| `next_id` | inteiro | próximo ID a atribuir (`store.add_task`) |
| `tasks` | lista | tarefas, por ordem de inserção |
| `id` | inteiro | identificador estável da tarefa |
| `text` | string | descrição livre |
| `done` | booleano | `false` ao criar, `true` após `done` |
| `priority` | string | `low`, `med` (por omissão) ou `high` |

Os campos correspondem à dataclass `Task` em `models.py`
(`id`, `text`, `done=False`, `priority="med"`), serializada com
`dataclasses.asdict`.

## Regras de leitura

`store._load` aplica estas regras, por esta ordem:

1. **Ficheiro inexistente** → `{"next_id": 1, "tasks": []}`. Uma instalação
   nova lista zero tarefas e a primeira tarefa criada recebe o ID `1`.
2. **`tasks` ausente** → assume lista vazia (`data.get("tasks", [])`).
3. **`next_id` ausente** → calcula `max(id) + 1`, ou `1` se não houver
   tarefas. Isto cobre ficheiros antigos escritos antes de `next_id` existir.
4. **Campos em falta numa tarefa** → `Task.from_dict` usa `False` para `done`
   e `"med"` para `priority`. `id` e `text` são obrigatórios: o acesso é
   direto (`data["id"]`, `data["text"]`), pelo que a sua ausência levanta
   `KeyError`.

O teste `test_old_file_without_priority` verifica os pontos 3 e 4.

## Regras de escrita

`store._save` reescreve o ficheiro completo a cada operação que altera estado
(`add`, `done`, `rm`). Não há escrita incremental nem ficheiro de lock.

- codificação UTF-8 explícita (`encoding="utf-8"`);
- `indent=2`, portanto indentação de dois espaços e uma linha por campo;
- `ensure_ascii=False`, logo acentos são gravados tal como escritos;
- a lista `tasks` fica pela ordem de inserção — a ordenação por prioridade
  acontece só na apresentação, em `cli.list_`.

`_load` normaliza o resultado para incluir apenas `next_id` e `tasks`, por
isso campos de topo desconhecidos desaparecem no primeiro `_save`.

## Edição manual

Como o formato é JSON simples, o ficheiro pode ser editado à mão. Duas
precauções decorrentes do código:

- manter `next_id` maior que todos os `id` existentes, para não reutilizar
  IDs (o valor só é recalculado quando o campo está ausente);
- usar apenas `low`, `med` ou `high` em `priority`, caso contrário `list`
  falha com `KeyError` ao consultar `_ORDER`.
