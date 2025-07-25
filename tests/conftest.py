# tests/conftest.py
import sys
import os

# dodaj katalog wyżej do ścieżki importów
root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, root)