import typer

from taskbot import store
from taskbot.models import PRIORITIES

app = typer.Typer(help="Task CLI.")

_ORDER = {p: i for i, p in enumerate(reversed(PRIORITIES))}


@app.command()
def add(
    text: str,
    priority: str = typer.Option("med", "--priority", "-p", help="low/med/high"),
) -> None:
    """Create a task."""
    if priority not in PRIORITIES:
        typer.echo(f"Invalid priority: {priority}", err=True)
        raise typer.Exit(1)
    task = store.add_task(text, priority)
    typer.echo(f"Task {task.id} created.")


@app.command("list")
def list_() -> None:
    """List tasks (high first)."""
    tasks = sorted(store.list_tasks(), key=lambda t: (_ORDER[t.priority], t.id))
    for t in tasks:
        mark = "x" if t.done else " "
        typer.echo(f"{t.id} [{mark}] ({t.priority}) {t.text}")


@app.command()
def done(task_id: int) -> None:
    """Mark a task as done."""
    try:
        store.mark_done(task_id)
    except KeyError:
        typer.echo(f"Task {task_id} does not exist.", err=True)
        raise typer.Exit(1)
    typer.echo(f"Task {task_id} done.")


@app.command()
def rm(task_id: int) -> None:
    """Remove a task."""
    try:
        store.remove_task(task_id)
    except KeyError:
        typer.echo(f"Task {task_id} does not exist.", err=True)
        raise typer.Exit(1)
    typer.echo(f"Task {task_id} removed.")
