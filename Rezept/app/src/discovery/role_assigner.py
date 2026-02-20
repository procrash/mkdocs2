"""Automatically assign models to roles (analyst, judge) based on capabilities."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field

from .model_classifier import ClassifiedModel, ModelCapability

logger = logging.getLogger(__name__)


@dataclass
class RoleAssignment:
    """Assignment of models to roles."""
    analysts: list[ClassifiedModel] = field(default_factory=list)
    judge: ClassifiedModel | None = None


def assign_roles(models: list[ClassifiedModel]) -> RoleAssignment:
    """Assign discovered models to analyst/judge roles.

    Strategy:
    - Judge: Prefer the largest model with tool_use capability.
    - Analysts: All other models with code_focused or basic capability.
    - If only 1 model: use it as sole analyst (no judge, no ensemble).
    - If 2 models: larger = judge, smaller = analyst.
    """
    if not models:
        logger.warning("No models available for role assignment")
        return RoleAssignment()

    if len(models) == 1:
        logger.info("Single model mode: %s as sole analyst", models[0].id)
        return RoleAssignment(analysts=models)

    # Sort by preference: large > medium > small, tool_use preferred for judge
    def judge_score(m: ClassifiedModel) -> int:
        score = 0
        if m.size_class == "large":
            score += 100
        elif m.size_class == "medium":
            score += 50
        if ModelCapability.TOOL_USE in m.capabilities:
            score += 30
        if ModelCapability.LONG_CONTEXT in m.capabilities:
            score += 20
        if ModelCapability.CODE_FOCUSED in m.capabilities:
            score += 10
        return score

    sorted_models = sorted(models, key=judge_score, reverse=True)
    judge = sorted_models[0]
    analysts = sorted_models[1:]

    # If we only have 2 models total, the judge also serves as analyst fallback
    if not analysts:
        analysts = [judge]
        judge = None

    logger.info("Judge: %s", judge.id if judge else "None (single-model mode)")
    for a in analysts:
        logger.info("Analyst: %s", a.id)

    return RoleAssignment(analysts=analysts, judge=judge)
