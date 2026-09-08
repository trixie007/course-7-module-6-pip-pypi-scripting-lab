import argparse
import json
import os
import requests
from datetime import datetime

class Task:
    def __init__(self, task_id: int, title: str, completed: bool = False):
        self.id = task_id
        self.title = title
        self.completed = completed

    def to_dict(self):
        return {"id": self.id, "title": self.title, "completed": self.completed}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["title"], data["completed"])


class TaskManager:
    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if not os.path.exists(self.storage_file):
            return []
        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError):
            return []

    def _save_tasks(self):
        with open(self.storage_file, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, title: str):
        new_id = max([t.id for t in self.tasks], default=0) + 1
        new_task = Task(new_id, title)
        self.tasks.append(new_task)
        self._save_tasks()
        print(f"Task added: [{new_id}] {title}")

    def complete_task(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                if task.completed:
                    print(f"Task #{task_id} is already marked as complete.")
                    return
                task.completed = True
                self._save_tasks()
                print(f"Task #{task_id} marked as complete.")
                return
        print(f"Error: Task with ID {task_id} not found.")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        print("\n--- Current Tasks ---")
        for t in self.tasks:
            status = "X" if t.completed else " "
            print(f"[{status}] ID {t.id}: {t.title}")
        print()

    def fetch_remote_sample(self):
        try:
            response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"Fetched External Sample Task: {data.get('title')}")
            else:
                print("Failed to fetch external sample.")
        except requests.RequestException as e:
            print(f"API request failed: {e}")


def build_parser():
    parser = argparse.ArgumentParser(description="CLI Task Manager Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available actions")

    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("--title", required=True, type=str, help="Title of the task")

    complete_parser = subparsers.add_parser("complete-task", help="Mark a task as complete")
    complete_parser.add_argument("--id", required=True, type=int, help="Task ID")

    subparsers.add_parser("list-tasks", help="List all tasks")
    subparsers.add_parser("fetch-sample", help="Fetch remote sample data via requests")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "add-task":
        manager.add_task(args.title)
    elif args.command == "complete-task":
        manager.complete_task(args.id)
    elif args.command == "list-tasks":
        manager.list_tasks()
    elif args.command == "fetch-sample":
        manager.fetch_remote_sample()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()