"""Parallelism control for concurrent opencode invocations."""
from __future__ import annotations
import asyncio
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class WorkerPool:
    """Controls the number of concurrent opencode processes."""

    def __init__(self, max_workers: int = 3):
        self._semaphore = asyncio.Semaphore(max_workers)
        self._max_workers = max_workers
        self._active = 0
        self._total_completed = 0
        self._lock = asyncio.Lock()

    @asynccontextmanager
    async def acquire(self, task_name: str = ""):
        """Acquire a worker slot."""
        await self._semaphore.acquire()
        async with self._lock:
            self._active += 1
        logger.debug(
            "Worker acquired for '%s' (%d/%d active)",
            task_name, self._active, self._max_workers,
        )
        try:
            yield
        finally:
            async with self._lock:
                self._active -= 1
                self._total_completed += 1
            self._semaphore.release()
            logger.debug(
                "Worker released for '%s' (%d/%d active, %d completed)",
                task_name, self._active, self._max_workers, self._total_completed,
            )

    @property
    def active_count(self) -> int:
        return self._active

    @property
    def completed_count(self) -> int:
        return self._total_completed
