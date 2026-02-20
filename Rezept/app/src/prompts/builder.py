"""Build complete prompts from templates and context."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field

from .registry import get_template, ensure_loaded

logger = logging.getLogger(__name__)


@dataclass
class PromptContext:
    """Context data for prompt rendering."""
    code_content: str = ""
    file_path: str = ""
    language: str = ""
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    function_signature: str = ""
    doxygen_section: str = ""
    file_listing: str = ""
    file_tree: str = ""
    key_files_content: str = ""
    section_name: str = ""
    page_listing: str = ""
    diagram_type: str = "classDiagram"
    # Judge-specific
    n_drafts: int = 0
    drafts_section: str = ""
    context: str = ""
    stakeholder: str = ""
    # Model-specific
    max_context_tokens: int = 32768


def build_prompt(
    stakeholder: str,
    doc_type: str,
    context: PromptContext,
) -> str | None:
    """Build a complete prompt from template and context."""
    ensure_loaded()
    template_fn = get_template(stakeholder, doc_type)
    if template_fn is None:
        logger.warning("No template found for %s/%s", stakeholder, doc_type)
        return None

    try:
        prompt = template_fn(context)
    except Exception as exc:
        logger.error("Error rendering %s/%s: %s", stakeholder, doc_type, exc)
        return None

    # Truncate if needed for model context
    max_chars = int(context.max_context_tokens * 3.5 * 0.7)  # 70% of context for prompt
    if len(prompt) > max_chars:
        logger.warning("Prompt truncated from %d to %d chars", len(prompt), max_chars)
        prompt = prompt[:max_chars] + "\n\n[... truncated due to context limit ...]"

    return prompt
