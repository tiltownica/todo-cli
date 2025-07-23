import json
import argparse
from pathlib import Path

DATA_FILE = Path("tasks.json")

def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []

def save_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=2, ensure_ascii=False))

def cmd_add(args):
    tasks = load_tasks()
    tasks.append({"text": args.text, "done": False})
    save_tasks(tasks)
    print(f'Dodano: "{args.text}"')

def cmd_list(_):
    tasks = load_tasks()
    if not tasks:
        print("Brak zadań.")
        return
    for i, t in enumerate(tasks, 1):
        mark = "✓" if t["done"] else " "
        print(f"{i}. [{mark}] {t['text']}")

def cmd_done(args):
    tasks = load_tasks()
    idx = args.index-1
    if 0 <= idx < len(tasks):
        tasks[idx]["done"] = True
        save_tasks(tasks)
        print(f"Oznaczono zadanie #{args.index} jako wykonane.")
    else:
        print("Błąd: nie ma takiego zadania.")

def cmd_remove(args):
    tasks = load_tasks()
    idx = args.index - 1
    if 0 <= idx < len(tasks):
        removed = tasks.pop(idx)
        save_tasks(tasks)
        print(f'Usunięto zadanie #{args.index}: "{removed["text"]}"')
    else:
        print("Błąd: nie ma takiego zadania.")

def cmd_edit(args):
    tasks = load_tasks()
    idx = args.index - 1
    if 0 <= idx < len(tasks):
        old = tasks[idx]["text"]
        tasks[idx]["text"] = args.text
        save_tasks(tasks)
        print(f'Zmieniono zadanie #{args.index}: "{old}" → "{args.text}"')
    else:
        print("Błąd: nie ma takiego zadania.")

def main():
    parser = argparse.ArgumentParser(prog="todo")
    sub = parser.add_subparsers(dest="command", required=True)
    p_add = sub.add_parser("add", help="Dodaj zadanie"); p_add.add_argument("text")
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