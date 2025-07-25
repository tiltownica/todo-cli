# tests/test_cli.py
import pytest
from typer.testing import CliRunner
from todo import app
from models import Task
from storage import DATA_FILE
import json

runner = CliRunner()

@pytest.fixture(autouse=True)
def clean_data(tmp_path, monkeypatch):
    # ustaw tmp_path jako miejsce na tasks.json
    fake = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DATA_FILE", str(fake))
    monkeypatch.setattr("storage.DATA_FILE", fake)
    yield

def test_add_and_List():
    # add
    res = runner.invoke(app, ["add", "Test1"])
    assert res.exit_code == 0
    assert "Dodano: 'Test1'" in res.stdout

    # List
    res = runner.invoke(app, ["list"])
    assert res.exit_code == 0
    assert "1. [ ] Test1" in res.stdout
    
def test_add_with_due_and_overdue_flag():
    # dodanie z terminem w przeszłości
    res = runner.invoke(app, ["add", "Old", "--due", "2000-01-01"])
    assert res.exit_code == 0
    assert "(due: 2000-01-01)" in res.stdout

    out = runner.invoke(app, ["list"])
    assert "⚠ Old" in out.stdout  # oznaczone ⚠

def test_done_and_remove_and_edit():
    runner.invoke(app, ["add", "A"])
    runner.invoke(app, ["add", "B"])

    # done
    res = runner.invoke(app, ["done", "1"])
    assert "oznaczone jako wykonane" in res.stdout

    # remove
    res = runner.invoke(app, ["remove", "2"])
    assert "Usunięto zadanie #2" in res.stdout

    # edit
    runner.invoke(app, ["add", "C"])
    res = runner.invoke(app, ["edit", "2", "C2"])
    assert "Zmieniono zadanie #2: 'C' → 'C2'" in res.stdout