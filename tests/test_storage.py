# tests/test_storage.py
import json
import tempfile
import os
import pytest

from storage import load_tasks, save_tasks, DATA_FILE
from models import Task

@pytest.fixture(autouse=True)
def tmp_data_file(tmp_path, monkeypatch):
    # Podmieniamy ścieżkę DATA_FILE na plik w tmp_path
    fake = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DATA_DILE", str(fake))
    monkeypatch.setattr("storage.DATA_FILE", fake)
    return fake

def test_save_and_load(tmp_data_file):
    # przygotuj dwie instalacje Task
    tasks = [Task(text="A"), Task(text="B", done=True, due="2025-07-30")]
    save_tasks(tasks)

    # sprawdź co się zapisało na dysku
    raw = json.loads(tmp_data_file.read_text(encoding="utf-8"))
    assert raw == [
        {"text": "A", "done": False, "due": None},
        {"text": "B", "done": True, "due": "2025-07-30"}
    ]

    # czy load_tasks odtwarza obiekty 
    loaded = load_tasks()
    assert loaded == tasks