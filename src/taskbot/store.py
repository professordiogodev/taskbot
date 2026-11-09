import json
import os
from pathlib import Path

from taskbot.models import Task


def default_path() -> Path:
    return Path(os.environ.get("TASKBOT_FILE", Path.home() / ".taskbot.json"))


def _load(path: Path) -> dict:
    if not path.exists():
        return {"next_id": 1, "tasks": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    tasks = data.get("tasks", [])
    next_id = data.get("next_id", max((t["id"] for t in tasks), default=0) + 1)
    return {"next_id": next_id, "tasks": tasks}


def _save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def list_tasks(path: Path | None = None) -> list[Task]:
    return [Task.from_dict(t) for t in _load(path or default_path())["tasks"]]


def add_task(text: str, priority: str = "med", path: Path | None = None) -> Task:
    path = path or default_path()
    data = _load(path)
    task = Task(id=data["next_id"], text=text, priority=priority)
    data["tasks"].append(task.to_dict())
    data["next_id"] += 1
    _save(path, data)
    return task


def mark_done(task_id: int, path: Path | None = None) -> Task:
    path = path or default_path()
    data = _load(path)
    for t in data["tasks"]:
        if t["id"] == task_id:
            t["done"] = True
            _save(path, data)
            return Task.from_dict(t)
    raise KeyError(task_id)


def remove_task(task_id: int, path: Path | None = None) -> None:
    path = path or default_path()
    data = _load(path)
    remaining = [t for t in data["tasks"] if t["id"] != task_id]
    if len(remaining) == len(data["tasks"]):
        raise KeyError(task_id)
    data["tasks"] = remaining
    _save(path, data)
