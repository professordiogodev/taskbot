import pytest
from typer.testing import CliRunner

from taskbot.cli import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def taskfile(tmp_path, monkeypatch):
    monkeypatch.setenv("TASKBOT_FILE", str(tmp_path / "t.json"))


def test_add_and_list():
    assert runner.invoke(app, ["add", "estudar"]).exit_code == 0
    out = runner.invoke(app, ["list"]).stdout
    assert "1 [ ] (med) estudar" in out


def test_done():
    runner.invoke(app, ["add", "a"])
    assert runner.invoke(app, ["done", "1"]).exit_code == 0
    assert "[x]" in runner.invoke(app, ["list"]).stdout


def test_done_unknown_id_fails():
    assert runner.invoke(app, ["done", "7"]).exit_code == 1


def test_rm():
    runner.invoke(app, ["add", "a"])
    assert runner.invoke(app, ["rm", "1"]).exit_code == 0
    assert runner.invoke(app, ["list"]).stdout.strip() == ""


def test_rm_unknown_id_fails():
    assert runner.invoke(app, ["rm", "7"]).exit_code == 1


def test_list_sorted_by_priority():
    runner.invoke(app, ["add", "baixa", "-p", "low"])
    runner.invoke(app, ["add", "alta", "-p", "high"])
    lines = runner.invoke(app, ["list"]).stdout.splitlines()
    assert "alta" in lines[0] and "baixa" in lines[1]


def test_invalid_priority():
    assert runner.invoke(app, ["add", "a", "-p", "x"]).exit_code == 1
