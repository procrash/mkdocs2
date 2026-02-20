"""Multi-model ensemble: query multiple analyst models in parallel."""
from __future__ import annotations
import asyncio
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Optional

from .opencode_runner import OpenCodeResult, run_opencode
from .semaphore import WorkerPool

logger = logging.getLogger(__name__)

# Type alias for failure callback: (model_id, error_msg) -> optional replacement model_id
FailureCallback = Callable[[str, str], Awaitable[Optional[str]]]


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
    failure_callback: Optional[FailureCallback] = None,
    max_tokens: int = 4096,
) -> EnsembleResult:
    """Query multiple models with the same prompt in parallel.

    Args:
        failure_callback: Called when a model fails all retries.
            Receives (model_id, error_message).
            Returns a replacement model_id to retry with, or None to skip.
        max_tokens: Maximum tokens for each model response.
    """
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
                max_tokens=max_tokens,
            )

    tasks = [query_single(mid) for mid in model_ids]
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    for model_id, response in zip(model_ids, responses):
        if isinstance(response, Exception):
            error_msg = str(response)
            logger.error("Exception querying %s: %s", model_id, error_msg)
            result.failed_models.append(model_id)

            # Call failure callback and try replacement
            if failure_callback:
                replacement = await failure_callback(model_id, error_msg)
                if replacement:
                    logger.info("Retrying with replacement model %s", replacement)
                    try:
                        retry_result = await query_single(replacement)
                        if retry_result.success and retry_result.output.strip():
                            result.drafts.append(retry_result)
                            result.successful_drafts.append(retry_result)
                            continue
                    except Exception as retry_exc:
                        logger.error("Replacement model %s also failed: %s", replacement, retry_exc)
            continue

        result.drafts.append(response)
        if response.success and response.output.strip():
            result.successful_drafts.append(response)
        else:
            error_msg = response.error or "Empty response"
            result.failed_models.append(model_id)

            if failure_callback:
                replacement = await failure_callback(model_id, error_msg)
                if replacement:
                    logger.info("Retrying with replacement model %s", replacement)
                    try:
                        retry_result = await query_single(replacement)
                        if retry_result.success and retry_result.output.strip():
                            result.drafts.append(retry_result)
                            result.successful_drafts.append(retry_result)
                            continue
                    except Exception as retry_exc:
                        logger.error("Replacement model %s also failed: %s", replacement, retry_exc)

    logger.info(
        "Ensemble: %d/%d models responded successfully",
        len(result.successful_drafts), len(model_ids),
    )
    return result
