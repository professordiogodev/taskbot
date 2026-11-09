import typer

from taskbot import store
from taskbot.models import PRIORITIES

app = typer.Typer(help="CLI de tarefas.")

_ORDER = {p: i for i, p in enumerate(reversed(PRIORITIES))}


@app.command()
def add(
    text: str,
    priority: str = typer.Option("med", "--priority", "-p", help="low/med/high"),
) -> None:
    """Cria uma tarefa."""
    if priority not in PRIORITIES:
        typer.echo(f"Prioridade inválida: {priority}", err=True)
        raise typer.Exit(1)
    task = store.add_task(text, priority)
    typer.echo(f"Tarefa {task.id} criada.")


@app.command("list")
def list_() -> None:
    """Lista tarefas (high primeiro)."""
    tasks = sorted(store.list_tasks(), key=lambda t: (_ORDER[t.priority], t.id))
    for t in tasks:
        mark = "x" if t.done else " "
        typer.echo(f"{t.id} [{mark}] ({t.priority}) {t.text}")


@app.command()
def done(task_id: int) -> None:
    """Marca como concluída."""
    try:
        store.mark_done(task_id)
    except KeyError:
        typer.echo(f"Tarefa {task_id} não existe.", err=True)
        raise typer.Exit(1)
    typer.echo(f"Tarefa {task_id} concluída.")


@app.command()
def rm(task_id: int) -> None:
    """Remove uma tarefa."""
    try:
        store.remove_task(task_id)
    except KeyError:
        typer.echo(f"Tarefa {task_id} não existe.", err=True)
        raise typer.Exit(1)
    typer.echo(f"Tarefa {task_id} removida.")
