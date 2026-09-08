import argparse
import json
import os
from datetime import datetime

# --- Task 1 & 2: Object-Oriented Design ---

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
        self._log_action(f"Added Task #{new_id}: '{title}'")
        print(f"✓ Task successfully added: [{new_id}] {title}")

    def complete_task(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                if task.completed:
                    print(f"Task #{task_id} is already marked as complete.")
                    return
                task.completed = True
                self._save_tasks()
                self._log_action(f"Completed Task #{task_id}")
                print(f"✓ Task #{task_id} marked as complete.")
                return
        print(f"✗ Error: Task with ID {task_id} not found.")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        print("\n--- Current Tasks ---")
        for t in self.tasks:
            status = "✓" if t.completed else " "
            print(f"[{status}] ID {t.id}: {t.title}")
        print()

    def _log_action(self, action: str):
        """Step 2 Log Generator: Writes daily log summary to file."""
        filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a") as f:
            f.write(f"[{timestamp}] {action}\n")


# --- CLI Parser Construction ---

def build_parser():
    parser = argparse.ArgumentParser(
        description="A lightweight CLI tool for managing tasks."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available actions")

    # Add Task Command
    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("--title", required=True, type=str, help="Title of the task")

    # Complete Task Command
    complete_parser = subparsers.add_parser("complete-task", help="Mark a task as completed")
    complete_parser.add_argument("--id", required=True, type=int, help="ID of the task to complete")

    # List Tasks Command
    subparsers.add_parser("list-tasks", help="Display all tasks")

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
    else:
        parser.print_help()


if __name__ == "__main__":
    main()