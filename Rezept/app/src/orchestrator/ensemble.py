"""Multi-model ensemble: query multiple analyst models in parallel."""
from __future__ import annotations
import asyncio
import logging
from dataclasses import dataclass, field

from .opencode_runner import OpenCodeResult, run_opencode
from .semaphore import WorkerPool

logger = logging.getLogger(__name__)


@dataclass
class EnsembleResult:
    """Results from querying multiple models."""
    drafts: list[OpenCodeResult] = field(default_factory=list)
    successful_drafts: list[OpenCodeResult] = field(default_factory=list)
    failed_models: list[str] = field(default_factory=list)


async def query_ensemble(
    prompt: str,
    model_ids: list[str],
    pool: WorkerPool,
    timeout: int = 120,
    max_retries: int = 3,
    retry_delay: int = 2,
    mock_mode: bool = False,
) -> EnsembleResult:
    """Query multiple models with the same prompt in parallel."""
    result = EnsembleResult()

    async def query_single(model_id: str) -> OpenCodeResult:
        async with pool.acquire(f"ensemble:{model_id}"):
            return await run_opencode(
                prompt=prompt,
                model_id=model_id,
                timeout=timeout,
                max_retries=max_retries,
                retry_delay=retry_delay,
                mock_mode=mock_mode,
            )

    tasks = [query_single(mid) for mid in model_ids]
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    for model_id, response in zip(model_ids, responses):
        if isinstance(response, Exception):
            logger.error("Exception querying %s: %s", model_id, response)
            result.failed_models.append(model_id)
            continue

        result.drafts.append(response)
        if response.success and response.output.strip():
            result.successful_drafts.append(response)
        else:
            result.failed_models.append(model_id)

    logger.info(
        "Ensemble: %d/%d models responded successfully",
        len(result.successful_drafts), len(model_ids),
    )
    return result
