# todo-cli

Prosta konsolowa aplikacja TODO list.

## Instalacja
    python -m venv venv
    source venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt   # (jeśli okaże się, że czegoś potrzebujesz)

## Użycie
    # dodanie zadania
    python todo.py add "Opis zadania"

    # wyświetlenie listy
    python todo.py list

    # oznaczenie zadania jako wykonane
    python todo.py done 1