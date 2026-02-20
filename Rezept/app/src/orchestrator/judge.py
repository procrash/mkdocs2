"""Judge module: select or merge the best response from multiple drafts."""
from __future__ import annotations
import logging

from ..prompts.builder import PromptContext, build_prompt
from .opencode_runner import OpenCodeResult, run_opencode
from .semaphore import WorkerPool

logger = logging.getLogger(__name__)


async def judge_drafts(
    drafts: list[OpenCodeResult],
    context_description: str,
    stakeholder: str,
    judge_model_id: str,
    pool: WorkerPool,
    timeout: int = 180,
    mock_mode: bool = False,
) -> str:
    """Use the judge model to merge/select the best draft.

    If only 1 draft, return it directly.
    If judge is unavailable, use heuristic selection.
    """
    if not drafts:
        logger.warning("No drafts to judge")
        return ""

    if len(drafts) == 1:
        logger.info("Single draft, skipping judge")
        return drafts[0].output

    # Build the judge prompt
    drafts_section = ""
    for i, draft in enumerate(drafts, 1):
        drafts_section += f"\n### Entwurf {i} (Modell: {draft.model_id})\n"
        drafts_section += draft.output
        drafts_section += "\n---\n"

    ctx = PromptContext(
        n_drafts=len(drafts),
        drafts_section=drafts_section,
        context=context_description,
        stakeholder=stakeholder,
    )

    prompt = build_prompt("judge", "merge", ctx)
    if not prompt:
        logger.warning("Could not build judge prompt, using heuristic")
        return _heuristic_select(drafts)

    async with pool.acquire("judge"):
        result = await run_opencode(
            prompt=prompt,
            model_id=judge_model_id,
            timeout=timeout,
            mock_mode=mock_mode,
        )

    if result.success and result.output.strip():
        logger.info("Judge merged %d drafts successfully", len(drafts))
        return result.output

    logger.warning("Judge failed, falling back to heuristic selection")
    return _heuristic_select(drafts)


def _heuristic_select(drafts: list[OpenCodeResult]) -> str:
    """Select the best draft using simple heuristics.

    Prefers: longer, more structured (more headers), with mermaid/latex.
    """
    def score(draft: OpenCodeResult) -> float:
        text = draft.output
        s = len(text) * 0.001  # Length
        s += text.count("##") * 5  # Headers
        s += text.count("```") * 3  # Code blocks
        s += text.count("mermaid") * 10  # Mermaid diagrams
        s += text.count("$") * 2  # LaTeX
        s += text.count("|") * 1  # Tables
        return s

    best = max(drafts, key=score)
    logger.info("Heuristic selected draft from %s (score: %.1f)", best.model_id, score(best))
    return best.output
