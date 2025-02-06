import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    """Represents a task for an agent to perform."""

    task: str  # The task description/prompt
    name: str  # The display name of the task
    id: Optional[str] = None  # Optional task identifier
    metadata: Optional[Dict[str, Any]] = None  # Any additional task metadata


class TaskManager:
    """Manages loading and accessing tasks."""

    def __init__(self, tasks_file: Path):
        self.tasks_file = tasks_file
        self.tasks: List[Task] = []
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load tasks from the JSONL file."""
        try:
            with open(self.tasks_file, "r") as f:
                for i, line in enumerate(f):
                    task_data = json.loads(line.strip())
                    # Create Task object with auto-generated ID if none exists
                    self.tasks.append(
                        Task(
                            task=task_data["task"],
                            name=task_data["name"],
                            id=task_data.get("id", f"task_{i}"),
                            metadata=task_data.get("metadata", {}),
                        )
                    )
        except Exception as e:
            raise RuntimeError(f"Failed to load tasks from {self.tasks_file}: {str(e)}")

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[Task]:
        """Get all available tasks."""
        return self.tasks.copy()  # Return a copy to prevent modification
