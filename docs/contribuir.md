# Contribuir

Este documento resume o fluxo de trabalho do repositório. A fonte de verdade
é o [`AGENTS.md`](../AGENTS.md); se os dois divergirem, vale o `AGENTS.md`.

## Comandos

Corre sempre a partir da raiz do repositório, usando o interpretador da
virtualenv local:

```bash
# testes
.venv/bin/python -m pytest -q

# lint + formatação
.venv/bin/python -m ruff check . && .venv/bin/python -m ruff format .
```

O `pytest` está configurado no `pyproject.toml` com
`pythonpath = ["src"]` e `testpaths = ["tests"]`, pelo que não é preciso
instalar o pacote nem definir `PYTHONPATH` para correr a suite. O `ruff` é
uma dependência do grupo `dev` (`[dependency-groups] dev = ["pytest",
"ruff"]`) e é apenas ferramenta de desenvolvimento, não dependência de
runtime.

Antes de abrir um pull request, os dois comandos devem passar: suite verde e
`ruff check` sem avisos, com o código já formatado por `ruff format`.

## Regras do projeto

Transcritas do `AGENTS.md`:

- **Funções públicas com type hints e um teste em `tests/`.** Qualquer função
  pública nova em `src/taskbot/` deve ter anotações de tipo e cobertura em
  `tests/`, seguindo o estilo de `store.add_task(text: str, priority: str =
  "med", path: Path | None = None) -> Task`.
- **Não adicionar dependências sem perguntar.** O `pyproject.toml` declara
  apenas `typer` (e `mcp[cli]`, `rank-bm25`) em runtime; `pytest` e `ruff` são
  de desenvolvimento. Uma dependência nova é uma decisão a discutir, não um
  detalhe de implementação.
- **Nunca alterar testes existentes para os fazer passar.** Se um teste falha,
  o problema está no código. Ajustar a asserção para verde esconde a regressão.

## Onde mexer

O código está dividido em três módulos, com responsabilidades distintas:

| Ficheiro | Responsabilidade |
| --- | --- |
| `src/taskbot/models.py` | dataclass `Task` e tupla `PRIORITIES` |
| `src/taskbot/store.py` | leitura/escrita do JSON e operações sobre tarefas |
| `src/taskbot/cli.py` | comandos Typer, validação de entrada, formatação de saída |

A separação explica-se pelos testes: `tests/test_store.py` exercita o `store`
diretamente, passando `path=tmp_path / "tasks.json"` como argumento
explícito, sem tocar no ambiente. `tests/test_cli.py` usa o `CliRunner` do
Typer e o fixture autouse `taskfile`, que define `TASKBOT_FILE` para um
ficheiro temporário. Ao acrescentares funcionalidade, mantém esta fronteira:
regras de apresentação e validação de argumentos em `cli.py`, persistência em
`store.py`.

## Checklist de alteração

1. Perceber o comportamento atual — `store._load` e `store._save` são o
   contrato do formato descrito em [`formato-ficheiro.md`](formato-ficheiro.md).
2. Implementar com type hints nas funções públicas.
3. Acrescentar o teste correspondente em `tests/` (sem editar os existentes).
4. Correr `.venv/bin/python -m pytest -q`.
5. Correr `.venv/bin/python -m ruff check . && .venv/bin/python -m ruff format .`.
6. Se o comportamento visível mudar, atualizar `cli.md` ou `formato-ficheiro.md`.
