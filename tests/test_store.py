import json

import pytest

from taskbot import store


@pytest.fixture
def path(tmp_path):
    return tmp_path / "tasks.json"


def test_missing_file_is_empty(path):
    assert store.list_tasks(path) == []


def test_add_assigns_incremental_ids(path):
    assert store.add_task("a", path=path).id == 1
    assert store.add_task("b", path=path).id == 2


def test_ids_never_reused_after_rm(path):
    store.add_task("a", path=path)
    store.add_task("b", path=path)
    store.remove_task(2, path)
    assert store.add_task("c", path=path).id == 3


def test_mark_done(path):
    store.add_task("a", path=path)
    assert store.mark_done(1, path).done is True
    assert store.list_tasks(path)[0].done is True


def test_done_unknown_id_raises(path):
    with pytest.raises(KeyError):
        store.mark_done(99, path)


def test_rm_unknown_id_raises(path):
    store.add_task("a", path=path)
    with pytest.raises(KeyError):
        store.remove_task(99, path)
    assert len(store.list_tasks(path)) == 1


def test_old_file_without_priority(path):
    path.write_text(json.dumps({"tasks": [{"id": 1, "text": "x", "done": False}]}))
    assert store.list_tasks(path)[0].priority == "med"
    assert store.add_task("y", path=path).id == 2
