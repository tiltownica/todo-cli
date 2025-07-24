import typer
import datetime
from typing import Optional
from models import Task
from storage import load_tasks, save_tasks

app = typer.Typer(help="Prosta konsolowa aplikacja TODO list z użyciem Typer")

@app.command()
def add(text: str, due: Optional[str] = typer.Option(None, help="Termin wykonania YYYY-MM-DD")):
    """Dodaj nowe zadanie"""
    tasks = load_tasks()
    due_str = None
    if due:
        try:
            due_date = datetime.datetime.strptime(due, "%Y-%m-%d").date()
            due_str = due_date.isoformat()
        except ValueError:
            typer.secho("Błąd: niewłaściwy format daty. Użyj YYYY-MM-DD.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        
    task = Task(text=text, due=due_str)
    tasks.append(task)
    save_tasks(tasks)
    msg = f"Dodano: '{text}'"
    if due_str:
        msg += f" (due: {due_str})"
    typer.secho(msg, fg=typer.colors.GREEN)

@app.command()
def list_(show_all: bool = typer.Option(True, help="Pokaż wszystkie zadania")):
    """Wyświetl listę zadań"""
    tasks = load_tasks()
    if not tasks:
        typer.secho("Brak zadań.", fg=typer.colors.YELLOW)
        return
    
    today = datetime.date.today()
    for i, t in enumerate(tasks, start=1):
        mark = "✓" if t.done else " "
        due = t.due or "-"
        overdue_flag = " ⚠ " if (t.due and not t.done and datetime.datetime.strptime(t.due, "%Y-%m-%d").date() < today) else ""
        typer.echo(f"{i}. [{mark}] {overdue_flag}{t.text} (due: {due})")

@app.command()
def done(index: int):
    """Oznacz zadanie jako wykonane"""
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        tasks[index-1].done = True
        save_tasks(tasks)
        typer.secho(f"Zadanie #{index} oznaczone jako wykonane.", fg=typer.colors.GREEN)
    else:
        typer.secho("Błąd: nie ma takiego zadania.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
@app.command()
def remove(index: int):
    """Usuń zadanie"""
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        removed = tasks.pop(index-1)
        save_tasks(tasks)
        typer.secho(f"Usunięto zadanie #{index}: '{removed.text}'", fg=typer.colors.GREEN)
    else:
        typer.secho("Błąd: nie ma takiego zadania.", fg=typer.colors.RED)

@app.command()
def edit(index: int, text: str):
    """Edytuj treść zadania"""
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        old = tasks[index-1].text
        tasks[index-1].text =text
        save_tasks(tasks)
        typer.secho(f"Zmieniono zadanie #{index}: '{old}' → '{text}'", fg=typer.colors.GREEN)
    else:
        typer.secho("Błąd: nie ma takiego zadania.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()