# taskbot
Task CLI in Python 3.10+, with Typer.

## Commands
- Tests: `.venv/bin/python -m pytest -q`
- Lint/format: `.venv/bin/python -m ruff check . && .venv/bin/python -m ruff format .`

## Architecture
- `src/taskbot/models.py` — Task dataclass
- `src/taskbot/store.py` — JSON persistence (TASKBOT_FILE variable)
- `src/taskbot/cli.py` — Typer commands

## Rules
- Public functions with type hints and a test in `tests/`.
- Do not add dependencies without asking.
- Never change existing tests to make them pass.
