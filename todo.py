import json
import argparse
from pathlib import Path
import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List

@dataclass
class Task:
    text: str
    done: bool = False
    due: Optional[str] = None

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

def cmd_add(args):
    tasks = load_tasks()
    due_str = None
    if args.due:
        try:
            due_date = datetime.datetime.strptime(args.due, "%Y-%m-%d").date()
            due_str = due_date.isoformat()
        except ValueError:
            print("Błąd: niewłaściwy format daty. Użyj YYYY-MM-DD.")
            return
    task = Task(text=args.text, due=due_str)
    tasks.append(task)
    save_tasks(tasks)
    msg = f'Dodano: "{args.text}"'
    if due_str:
        msg += f' (due: {due_str})'
    print(msg)

def cmd_list(_):
    tasks = load_tasks()
    if not tasks:
        print("Brak zadań.")
        return
    today = datetime.date.today()
    for i, t in enumerate(tasks, 1):
        mark = "✓" if t.done else " "
        due = t.due
        overdue = ""
        if due and not t["done"]:
            due_date = datetime.datetime.strptime(due, "%Y-%m-%d").date()
            if due_date < today:
                overdue = " ⚠ "
        due_part = f" (due:{due})" if due else ""
        print(f"{i}. [{mark}] {overdue}{t.text}{due_part}")

def cmd_done(args):
    tasks = load_tasks()
    idx = args.index-1
    if 0 <= idx < len(tasks):
        tasks[idx].done = True
        save_tasks(tasks)
        print(f"Oznaczono zadanie #{args.index} jako wykonane.")
    else:
        print("Błąd: nie ma takiego zadania.")

def cmd_remove(args):
    tasks = load_tasks()
    idx = args.index - 1
    if 0 <= idx < len(tasks):
        removed: Task = tasks.pop(idx)
        save_tasks(tasks)
        print(f'Usunięto zadanie #{args.index}: "{removed.text}"')
    else:
        print("Błąd: nie ma takiego zadania.")

def cmd_edit(args):
    tasks = load_tasks()
    idx = args.index - 1
    if 0 <= idx < len(tasks):
        old = tasks[idx].text
        tasks[idx].text = args.text
        save_tasks(tasks)
        print(f'Zmieniono zadanie #{args.index}: "{old}" → "{args.text}"')
    else:
        print("Błąd: nie ma takiego zadania.")

def main():
    parser = argparse.ArgumentParser(prog="todo")
    sub = parser.add_subparsers(dest="command", required=True)
    p_add = sub.add_parser("add", help="Dodaj zadanie")
    p_add.add_argument("text", help="Treść zadania")
    p_add.add_argument(
        "--due",
        help="Termin wykonania w formacie YYYY-MM-DD",
        required=False
    )
    p_list = sub.add_parser("list", help="Pokaż zadania")
    p_done = sub.add_parser("done", help="Oznacz zadanie"); p_done.add_argument("index", type=int)
    p_remove = sub.add_parser("remove", help="Usuń zadanie")
    p_remove.add_argument("index", type=int, help="Numer zadania do usunięcia")
    p_edit = sub.add_parser("edit", help="Edytuj treść zadania")
    p_edit.add_argument("index", type=int, help="Numer zadania do edycji")
    p_edit.add_argument("text", help="Nowa treść zadania")
    args = parser.parse_args()
    if args.command == "add": 
        cmd_add(args)
    elif args.command == "list": 
        cmd_list(args)
    elif args.command == "done": 
        cmd_done(args)
    elif args.command == "remove":
        cmd_remove(args)
    elif args.command == "edit":
        cmd_edit(args)

if __name__ == "__main__":
    main()