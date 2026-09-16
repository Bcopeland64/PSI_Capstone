"""Task service layer."""
from src.data_handler import load_tasks, save_tasks
from src.models.entities import Task, Priority


class TaskService:
    """Business logic for managing tasks."""

    def __init__(self, data_path):
        self.data_path = data_path
        self.tasks = load_tasks(data_path)

    def _next_id(self):
        return max((t.id for t in self.tasks), default=0) + 1

    def _persist(self):
        save_tasks(self.tasks, self.data_path)

    def add(self, title, priority="medium"):
        task = Task(id=self._next_id(), title=title, priority=Priority(priority))
        self.tasks.append(task)
        self._persist()
        return task

    def list_all(self, done=None):
        if done is None:
            return list(self.tasks)
        return [t for t in self.tasks if t.done == done]

    def get(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                return t
        raise KeyError(f"Task {task_id} not found")

    def complete(self, task_id):
        task = self.get(task_id)
        task.mark_done()
        self._persist()
        return task

    def delete(self, task_id):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) == before:
            raise KeyError(f"Task {task_id} not found")
        self._persist()
