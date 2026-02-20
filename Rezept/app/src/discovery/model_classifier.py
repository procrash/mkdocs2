"""Classify discovered models by their capabilities."""
from __future__ import annotations
import logging
import re
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ModelCapability(str, Enum):
    TOOL_USE = "tool_use"
    LONG_CONTEXT = "long_context"
    CODE_FOCUSED = "code_focused"
    VISION = "vision"
    BASIC = "basic"


@dataclass
class ClassifiedModel:
    """A model with inferred capabilities."""
    id: str
    capabilities: list[ModelCapability] = field(default_factory=list)
    estimated_context: int = 4096
    provider: str = ""
    size_class: str = "unknown"  # small, medium, large


# Patterns for heuristic classification
_CODE_PATTERNS = re.compile(
    r"(code|coder|starcoder|codellama|deepseek-coder|wizard-?code|phind|codestral)",
    re.IGNORECASE,
)
_LARGE_PATTERNS = re.compile(
    r"(70b|72b|65b|40b|34b|mixtral|qwen2?\.?5?-72|llama-?3\.?[12]?-?70|opus|sonnet)",
    re.IGNORECASE,
)
_MEDIUM_PATTERNS = re.compile(
    r"(13b|14b|22b|27b|8x7b|gemma-?2?-?27)",
    re.IGNORECASE,
)
_TOOL_PATTERNS = re.compile(
    r"(qwen2?\.?5|llama-?3\.?[12]|mistral-?(large|medium)|gemma-?2|claude|gpt-?4|command-?r)",
    re.IGNORECASE,
)
_LONG_CTX_PATTERNS = re.compile(
    r"(qwen2?\.?5|llama-?3\.?[12]|yi-?34|mistral-?(large|medium)|claude|gpt-?4|128k|131072|200k)",
    re.IGNORECASE,
)
_VISION_PATTERNS = re.compile(
    r"(llava|vision|vl$|vl-|bakllava|cogvlm|fuyu|moondream)",
    re.IGNORECASE,
)


def classify_model(model_id: str) -> ClassifiedModel:
    """Classify a single model by its ID using heuristics."""
    caps: list[ModelCapability] = []
    ctx = 4096
    size = "small"

    if _CODE_PATTERNS.search(model_id):
        caps.append(ModelCapability.CODE_FOCUSED)
    if _VISION_PATTERNS.search(model_id):
        caps.append(ModelCapability.VISION)
    if _TOOL_PATTERNS.search(model_id):
        caps.append(ModelCapability.TOOL_USE)
    if _LONG_CTX_PATTERNS.search(model_id):
        caps.append(ModelCapability.LONG_CONTEXT)
        ctx = 65536

    if _LARGE_PATTERNS.search(model_id):
        size = "large"
        if ModelCapability.LONG_CONTEXT not in caps:
            ctx = 32768
        if ModelCapability.CODE_FOCUSED not in caps:
            caps.append(ModelCapability.CODE_FOCUSED)
    elif _MEDIUM_PATTERNS.search(model_id):
        size = "medium"
        ctx = max(ctx, 16384)

    if not caps:
        caps.append(ModelCapability.BASIC)

    return ClassifiedModel(
        id=model_id,
        capabilities=caps,
        estimated_context=ctx,
        size_class=size,
    )


def classify_models(model_ids: list[str]) -> list[ClassifiedModel]:
    """Classify a list of model IDs."""
    return [classify_model(mid) for mid in model_ids]
