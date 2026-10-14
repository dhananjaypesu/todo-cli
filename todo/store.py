"""JSON-file storage for tasks."""

import json
from pathlib import Path

DEFAULT_PATH = Path.home() / ".todo.json"


class TaskStore:
    def __init__(self, path=DEFAULT_PATH):
        self.path = Path(path)
        self.tasks = self._load()

    def _load(self):
        if not self.path.exists():
            return []
        with self.path.open() as f:
            return json.load(f)

    def save(self):
        with self.path.open("w") as f:
            json.dump(self.tasks, f, indent=2)

    def add(self, title):
        next_id = max((t["id"] for t in self.tasks), default=0) + 1
        task = {"id": next_id, "title": title, "done": False}
        self.tasks.append(task)
        self.save()
        return task

    def complete(self, task_id):
        task = self._get(task_id)
        task["done"] = True
        self.save()
        return task

    def remove(self, task_id):
        task = self._get(task_id)
        self.tasks.remove(task)
        self.save()
        return task

    def pending(self):
        return [t for t in self.tasks if not t["done"]]

    def _get(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        raise KeyError(f"No task with id {task_id}")
