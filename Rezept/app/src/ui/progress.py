"""Shared progress tracking abstraction for CLI and TUI."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ProgressTask:
    """A trackable progress task."""
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0  # 0.0 to 1.0
    detail: str = ""
    error: str = ""


@dataclass
class ProgressTracker:
    """Track overall pipeline progress."""
    tasks: dict[str, ProgressTask] = field(default_factory=dict)
    phase: str = "idle"
    phase_progress: float = 0.0
    _callbacks: list[Callable] = field(default_factory=list)

    def add_callback(self, callback: Callable) -> None:
        """Register a progress update callback."""
        self._callbacks.append(callback)

    def _notify(self) -> None:
        """Notify all registered callbacks."""
        for cb in self._callbacks:
            try:
                cb(self)
            except Exception as exc:
                logger.debug("Progress callback error: %s", exc)

    def set_phase(self, phase: str, progress: float = 0.0) -> None:
        """Set the current pipeline phase."""
        self.phase = phase
        self.phase_progress = progress
        self._notify()

    def add_task(self, task_id: str, description: str) -> ProgressTask:
        """Add a new trackable task."""
        task = ProgressTask(id=task_id, description=description)
        self.tasks[task_id] = task
        self._notify()
        return task

    def update_task(
        self,
        task_id: str,
        status: TaskStatus | None = None,
        progress: float | None = None,
        detail: str | None = None,
        error: str | None = None,
    ) -> None:
        """Update a task's status."""
        task = self.tasks.get(task_id)
        if not task:
            return
        if status is not None:
            task.status = status
        if progress is not None:
            task.progress = progress
        if detail is not None:
            task.detail = detail
        if error is not None:
            task.error = error
        self._notify()

    @property
    def total_tasks(self) -> int:
        return len(self.tasks)

    @property
    def completed_tasks(self) -> int:
        return sum(
            1 for t in self.tasks.values()
            if t.status in (TaskStatus.SUCCESS, TaskStatus.FAILED, TaskStatus.SKIPPED)
        )

    @property
    def success_count(self) -> int:
        return sum(1 for t in self.tasks.values() if t.status == TaskStatus.SUCCESS)

    @property
    def failed_count(self) -> int:
        return sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)

    @property
    def overall_progress(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return self.completed_tasks / self.total_tasks
