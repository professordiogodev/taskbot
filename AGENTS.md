# taskbot
CLI de tarefas em Python 3.10+, com Typer.

## Comandos
- Testes: `.venv/bin/python -m pytest -q`
- Lint/format: `.venv/bin/python -m ruff check . && .venv/bin/python -m ruff format .`

## Arquitetura
- `src/taskbot/models.py` — dataclass Task
- `src/taskbot/store.py` — persistência JSON (variável TASKBOT_FILE)
- `src/taskbot/cli.py` — comandos Typer

## Regras
- Funções públicas com type hints e um teste em `tests/`.
- Não adicionar dependências sem perguntar.
- Nunca alterar testes existentes para os fazer passar.
