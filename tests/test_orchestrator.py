"""Tests for the orchestration engine."""
import asyncio

import pytest

from src.orchestrator.opencode_runner import run_opencode, OpenCodeResult
from src.orchestrator.semaphore import WorkerPool
from src.orchestrator.ensemble import query_ensemble
from src.orchestrator.judge import _heuristic_select


class TestOpenCodeRunner:
    def test_mock_mode(self):
        result = asyncio.run(run_opencode(
            prompt="Test prompt",
            model_id="test-model",
            mock_mode=True,
        ))
        assert result.success is True
        assert "Mock Documentation" in result.output
        assert result.model_id == "test-model"

    def test_mock_contains_prompt_info(self):
        prompt = "x" * 100
        result = asyncio.run(run_opencode(prompt=prompt, model_id="m1", mock_mode=True))
        assert "100 characters" in result.output


class TestWorkerPool:
    def test_basic_acquire_release(self):
        async def _test():
            pool = WorkerPool(max_workers=2)
            assert pool.active_count == 0
            async with pool.acquire("test"):
                assert pool.active_count == 1
            assert pool.active_count == 0
            assert pool.completed_count == 1

        asyncio.run(_test())

    def test_concurrency_limit(self):
        async def _test():
            pool = WorkerPool(max_workers=2)
            started = []
            finished = []

            async def worker(name: str):
                async with pool.acquire(name):
                    started.append(name)
                    await asyncio.sleep(0.05)
                    finished.append(name)

            await asyncio.gather(worker("a"), worker("b"), worker("c"))
            assert len(finished) == 3

        asyncio.run(_test())


class TestEnsemble:
    def test_mock_ensemble(self):
        async def _test():
            pool = WorkerPool(max_workers=3)
            result = await query_ensemble(
                prompt="Test",
                model_ids=["model-a", "model-b"],
                pool=pool,
                mock_mode=True,
            )
            assert len(result.successful_drafts) == 2
            assert len(result.failed_models) == 0

        asyncio.run(_test())


class TestJudge:
    def test_heuristic_select(self):
        drafts = [
            OpenCodeResult(success=True, output="Short.", model_id="a"),
            OpenCodeResult(
                success=True,
                output="## Long Document\n\nWith **headers** and\n\n```mermaid\ngraph TD\n```\n\n| Col | Col |\n|---|---|\n",
                model_id="b",
            ),
        ]
        best = _heuristic_select(drafts)
        assert "Long Document" in best
