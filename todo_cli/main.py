#!/usr/bin/env python3
"""Simple TODO list CLI.

Usage::

    python main.py add "Buy milk"
    python main.py list

Tasks are persisted in a JSON file (default: tasks.json) located next to this script.
You can override the storage path via the --file option, e.g.:

    python main.py --file /tmp/mytasks.json add "Walk the dog"
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

DEFAULT_TASK_FILE = Path(__file__).parent / "tasks.json"


def load_tasks(path: Path = DEFAULT_TASK_FILE) -> List[str]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
        if isinstance(data, list):
            return [str(item) for item in data]
        # fallthrough: invalid format resets file
    except json.JSONDecodeError:
        pass
    return []


def save_tasks(tasks: List[str], path: Path = DEFAULT_TASK_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        json.dump(tasks, fp, ensure_ascii=False, indent=2)


def add_task(task: str, path: Path = DEFAULT_TASK_FILE) -> None:
    tasks = load_tasks(path)
    tasks.append(task)
    save_tasks(tasks, path)
    print(f"Added task #{len(tasks)}: {task}")


def list_tasks(path: Path = DEFAULT_TASK_FILE) -> None:
    tasks = load_tasks(path)
    if not tasks:
        print("No tasks found.")
        return
    for idx, task in enumerate(tasks, start=1):
        print(f"{idx}. {task}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple TODO list CLI")
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_TASK_FILE,
        help="Path to tasks JSON file (default: %(default)s)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("task", help="Task description")

    subparsers.add_parser("list", help="List all tasks")

    return parser


def main(argv: list[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    task_file: Path = args.file

    if args.command == "add":
        add_task(args.task, task_file)
    elif args.command == "list":
        list_tasks(task_file)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main() 