import json
import tempfile
from pathlib import Path

import pytest

from todo_cli.main import load_tasks, save_tasks, add_task, list_tasks


def test_add_and_load_tasks(tmp_path: Path, capsys):
    task_file = tmp_path / "tasks.json"
    add_task("Buy milk", task_file)
    add_task("Walk the dog", task_file)

    tasks = load_tasks(task_file)
    assert tasks == ["Buy milk", "Walk the dog"]

    captured = capsys.readouterr()
    assert "Added task #2" in captured.out


def test_save_tasks(tmp_path: Path):
    task_file = tmp_path / "tasks.json"
    save_tasks(["Task A", "Task B"], task_file)
    with task_file.open(encoding="utf-8") as fp:
        data = json.load(fp)
    assert data == ["Task A", "Task B"] 