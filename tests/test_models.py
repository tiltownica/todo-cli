# tests/test_models.py
import pytest
from models import Task

def test_task_defaults():
    t = Task(text="Hello")
    assert t.text == "Hello"
    assert t.done is False
    assert t.due is None

def test_task_full():
    t = Task(text="Buy milk", done=True, due="2025-07-30")
    assert t.text =="Buy milk"
    assert t.done is True
    assert t.due == "2025-07-30"