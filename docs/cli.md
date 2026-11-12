# Referência da CLI

O `taskbot` é uma aplicação [Typer] exposta em `src/taskbot/cli.py`
(`app = typer.Typer(help="CLI de tarefas.")`). O ponto de entrada instalado
está declarado no `pyproject.toml`:

```toml
[project.scripts]
taskbot = "taskbot.cli:app"
```

Nos exemplos abaixo, `taskbot` designa esse script de consola (em
`.venv/bin/taskbot` depois de `uv sync`); o módulo em si não tem bloco
`__main__`, por isso `python -m taskbot.cli` não arranca a aplicação.

## Comandos

| Comando | Argumentos / opções | Efeito |
| --- | --- | --- |
| `taskbot add TEXTO` | `--priority`, `-p` (por omissão `med`) | cria a tarefa e imprime `Tarefa N criada.` |
| `taskbot list` | — | lista as tarefas, `high` primeiro |
| `taskbot done ID` | inteiro | marca como concluída e imprime `Tarefa N concluída.` |
| `taskbot rm ID` | inteiro | remove e imprime `Tarefa N removida.` |

Notas confirmadas no código:

- a função de `list` chama-se `list_` e é registada explicitamente com
  `@app.command("list")`, porque `list` é um nome builtin;
- `add` aceita o texto como argumento posicional, sem aspas obrigatórias na
  shell além das necessárias para preservar espaços;
- `done` sobre uma tarefa já concluída não é erro: volta a gravar
  `done: true` e imprime a mesma mensagem.

Exemplo de sessão:

```console
$ taskbot add "estudar agentes" -p high
Tarefa 1 criada.
$ taskbot add "comprar pão"
Tarefa 2 criada.
$ taskbot list
1 [ ] (high) estudar agentes
2 [ ] (med) comprar pão
$ taskbot done 2
Tarefa 2 concluída.
$ taskbot list
1 [ ] (high) estudar agentes
2 [x] (med) comprar pão
```

## Formato da listagem

Cada linha tem o formato `{id} [{mark}] ({priority}) {text}`, onde `mark` é
`x` se `done` for verdadeiro e um espaço caso contrário:

```python
mark = "x" if t.done else " "
typer.echo(f"{t.id} [{mark}] ({t.priority}) {t.text}")
```

O `[ ]` aparece portanto com dois caracteres — colchetes com um espaço no
meio. Sem tarefas, `list` não imprime nada (saída vazia, código `0`).

A ordenação vem de `sorted(..., key=lambda t: (_ORDER[t.priority], t.id))`,
com `_ORDER` a dar `high = 0`, `med = 1`, `low = 2`. Empates de prioridade
são desfeitos pelo ID mais baixo primeiro. Tarefas concluídas continuam a
aparecer, na sua posição normal.

## Prioridades

Os valores válidos são exatamente os de `models.PRIORITIES`:

```python
PRIORITIES = ("low", "med", "high")
```

A prioridade por omissão é `med`, tanto na opção da CLI
(`typer.Option("med", "--priority", "-p", ...)`) como no valor por omissão da
dataclass `Task`. Um valor fora da lista é rejeitado **antes** de escrever no
ficheiro:

```console
$ taskbot add "a" -p x
Prioridade inválida: x
$ echo $?
1
```

A mensagem é escrita em `stderr` (`err=True`), tal como as mensagens de erro
dos comandos `done` e `rm`.

## Códigos de saída

| Situação | Código |
| --- | --- |
| Comando executado com sucesso | `0` |
| `add` com prioridade inválida | `1` |
| `done ID` com ID inexistente | `1` |
| `rm ID` com ID inexistente | `1` |

Nos dois últimos casos a CLI imprime `Tarefa N não existe.` em `stderr`. O
`KeyError` lançado por `store.mark_done` / `store.remove_task` é apanhado em
`cli.py` e convertido em `typer.Exit(1)`, mantendo a camada de persistência
independente da interface.

[Typer]: https://typer.tiangolo.com/
