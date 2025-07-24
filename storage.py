# storage.py
import json
from pathlib import Path
from dataclasses import asdict
from typing import List
from models import Task

DATA_FILE = Path("tasks.json")

def load_tasks() -> List[Task]:
    if DATA_FILE.exists():
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return [Task(**item) for item in raw]
    return []

def save_tasks(tasks: List[Task]):
    data = [asdict(t) for t in tasks]
    DATA_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
