"""Classify discovered models by their capabilities."""
from __future__ import annotations
import logging
import re
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ModelCapability(str, Enum):
    TOOL_USE = "tool_use"
    INSTRUCT = "instruct"
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
_INSTRUCT_PATTERNS = re.compile(
    r"(instruct|chat|it$|-it-|assistant|rlhf|dpo|sft|hermes|openhermes|nous|neural-chat|zephyr|openchat|vicuna|alpaca)",
    re.IGNORECASE,
)


def classify_model(
    model_id: str,
    detected_context: int = 0,
    detected_caps: set[str] | None = None,
) -> ClassifiedModel:
    """Classify a single model by its ID using heuristics.

    If *detected_context* > 0 (obtained from the server API), it overrides the
    heuristic estimate.  A detected context length ≥ 32768 also triggers the
    LONG_CONTEXT capability flag.

    *detected_caps* can contain capability values (e.g. {"tool_use", "instruct"})
    obtained from active probing, which will be merged in.
    """
    caps: list[ModelCapability] = []
    ctx = 4096
    size = "small"

    if _CODE_PATTERNS.search(model_id):
        caps.append(ModelCapability.CODE_FOCUSED)
    if _VISION_PATTERNS.search(model_id):
        caps.append(ModelCapability.VISION)
    if _TOOL_PATTERNS.search(model_id):
        caps.append(ModelCapability.TOOL_USE)
    if _INSTRUCT_PATTERNS.search(model_id):
        caps.append(ModelCapability.INSTRUCT)
    if _LONG_CTX_PATTERNS.search(model_id):
        caps.append(ModelCapability.LONG_CONTEXT)
        ctx = 65536

    if _LARGE_PATTERNS.search(model_id):
        size = "large"
        if ModelCapability.LONG_CONTEXT not in caps:
            ctx = 32768
        if ModelCapability.CODE_FOCUSED not in caps:
            caps.append(ModelCapability.CODE_FOCUSED)
        # Large models are almost always instruct-tuned
        if ModelCapability.INSTRUCT not in caps:
            caps.append(ModelCapability.INSTRUCT)
    elif _MEDIUM_PATTERNS.search(model_id):
        size = "medium"
        ctx = max(ctx, 16384)

    # Server-detected context overrides heuristic
    if detected_context > 0:
        ctx = detected_context
        if detected_context >= 32768 and ModelCapability.LONG_CONTEXT not in caps:
            caps.append(ModelCapability.LONG_CONTEXT)

    # Merge detected capabilities from active probing
    if detected_caps:
        for cap_str in detected_caps:
            try:
                cap = ModelCapability(cap_str)
                if cap not in caps:
                    caps.append(cap)
            except ValueError:
                pass

    if not caps:
        caps.append(ModelCapability.BASIC)

    return ClassifiedModel(
        id=model_id,
        capabilities=caps,
        estimated_context=ctx,
        size_class=size,
    )


def classify_models(
    model_ids: list[str],
    detected_contexts: dict[str, int] | None = None,
    detected_capabilities: dict[str, set[str]] | None = None,
) -> list[ClassifiedModel]:
    """Classify a list of model IDs.

    *detected_contexts* maps model_id → context_length as discovered from the server.
    *detected_capabilities* maps model_id → set of capability strings from active probing.
    """
    ctx_map = detected_contexts or {}
    caps_map = detected_capabilities or {}
    return [
        classify_model(mid, ctx_map.get(mid, 0), caps_map.get(mid))
        for mid in model_ids
    ]
