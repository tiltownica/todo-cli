# todo-cli

[![Python Tests](https://github.com/tiltownica/todo-cli/actions/workflows/python-tests.yml/badge.svg)](https://github.com/tiltownica/todo-cli/actions)

**Prosta, konsolowa aplikacja TODO list** napisana w Pythonie z użyciem [Typer](https://typer.tiangolo.com/).

## Funkcjonalności

- Dodawanie zadań (`add`), opcjonalnie z terminem (`--due YYYY-MM-DD`).
- Wyświetlanie listy zadań (`list`), z oznaczeniem wykonanych.
- Oznaczanie zadania jako wykonane (`done <nr>`).
- Usuwanie zadania (`remove <nr>`).
- Edycja treści zadania (`edit <nr> "Nowa treść"`).
- Przechowywanie zadań w `tasks.json` w formacie JSON.
- Obsługa polskich znaków (UTF-8).
- Automatyczne testy jednostkowe i integracyjne (`pytest`).
- CI z GitHub Actions uruchamiające testy przy każdym pushu.

## Instalacja

```bash
# Sklonuj repo
git clone git@github.com:tiltownica/todo-cli.git
cd todo-cli
```

## Utwórz i aktywuj wirtualne środowisko

```bash
python -m venv venv
# Linux/macOS / Git Bash:
source venv/bin/activate
# Windows PowerShell:
# .\venv\Scripts\Activate.ps1

# Zainstaluj zależności
pip install -r requirements.txt
```

## Użycie

Po instalacji możesz wywoływać polecenia:

```bash
# dodanie zadania
python todo.py add "Kup wodę"

# dodanie zadania z terminem
python todo.py add "Wyślij raport" --due 2025-07-30

# wyświetlenie wszystkich zadań
python todo.py list

# oznaczenie zadania jako wykonane
python todo.py done 1

# usunięcie zadania
python todo.py remove 2

# edycja treści zadania
python todo.py edit 3 "Kup gazowaną wodę" 
```

## Testy
Uruchom wszystkie testy jednostkowe i integracyjne:

```bash
pytest -q
```

## CI/CD

Testy uruchamiane są automatycznie przy każdym pushu do gałęzi `main` dzięki GitHub Actions.  
Konfiguracja znajduje się w pliku:

```yaml
.github/workflows/python-tests.yml
```

