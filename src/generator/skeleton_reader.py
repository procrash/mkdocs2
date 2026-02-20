"""Read skeleton pages and extract content guidelines for LLM prompt context.

Parses the ``!!! tip "Inhaltsrichtlinie"`` admonition blocks from skeleton
markdown files and provides them as structured context for prompt templates.
"""
from __future__ import annotations
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# Pattern to extract the admonition block:
# !!! tip "Inhaltsrichtlinie"
#     indented text (possibly multi-line)
_GUIDELINE_PATTERN = re.compile(
    r'!!! tip "Inhaltsrichtlinie"\n((?:    .+\n|[ \t]*\n)+)',
    re.MULTILINE,
)


def _extract_guideline(markdown: str) -> str:
    """Extract the Inhaltsrichtlinie text from a markdown page.

    Returns the guideline text with leading 4-space indentation stripped,
    or empty string if none found.
    """
    m = _GUIDELINE_PATTERN.search(markdown)
    if not m:
        return ""
    raw = m.group(1)
    # Strip the 4-space admonition indent from each line
    lines = []
    for line in raw.split("\n"):
        if line.startswith("    "):
            lines.append(line[4:])
        elif line.strip() == "":
            lines.append("")
        else:
            break  # end of indented block
    # Strip trailing blank lines
    while lines and lines[-1].strip() == "":
        lines.pop()
    return "\n".join(lines)


def load_all_guidelines(docs_dir: Path) -> dict[str, str]:
    """Read all skeleton markdown files and extract their Inhaltsrichtlinien.

    Args:
        docs_dir: The ``docs/`` directory inside the output project.

    Returns:
        dict mapping relative_path (e.g. ``"getting-started/installation.md"``)
        to the extracted guideline text.
    """
    guidelines: dict[str, str] = {}
    if not docs_dir.is_dir():
        logger.warning("docs_dir does not exist: %s", docs_dir)
        return guidelines

    for md_file in sorted(docs_dir.rglob("*.md")):
        rel = md_file.relative_to(docs_dir).as_posix()
        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            logger.debug("Cannot read %s: %s", md_file, exc)
            continue
        guideline = _extract_guideline(text)
        if guideline:
            guidelines[rel] = guideline

    logger.info("Loaded %d content guidelines from %s", len(guidelines), docs_dir)
    return guidelines


def find_matching_page(
    content_description: str,
    guidelines: dict[str, str],
) -> str | None:
    """Find the best-matching skeleton page for a content description.

    Uses simple keyword overlap scoring.  Returns the page path with the
    highest overlap, or ``None`` if no reasonable match is found.

    Args:
        content_description: Short description of the content to place
            (e.g. a file path or topic sentence).
        guidelines: dict from :func:`load_all_guidelines`.
    """
    if not guidelines:
        return None

    desc_words = set(content_description.lower().split())
    best_path: str | None = None
    best_score = 0

    for page_path, guideline_text in guidelines.items():
        # Score = keyword overlap between description and (path + guideline)
        page_words = set(page_path.lower().replace("/", " ").replace("-", " ").replace(".", " ").split())
        guideline_words = set(guideline_text.lower().split())
        candidate_words = page_words | guideline_words
        score = len(desc_words & candidate_words)
        if score > best_score:
            best_score = score
            best_path = page_path

    # Require at least 2 keyword matches for a meaningful result
    if best_score < 2:
        return None
    return best_path


def build_skeleton_context(docs_dir: Path, max_chars: int = 0) -> str:
    """Build a compact context string listing all pages with their guidelines.

    Intended to be injected into LLM prompts so the model knows which
    documentation pages exist and what belongs where.

    Args:
        docs_dir: The ``docs/`` directory.
        max_chars: If >0, truncate the output to this many characters.

    Returns:
        Formatted string like::

            ## Seite: getting-started/installation.md
            Richtlinie: Zielgruppe: Neue Benutzer ...

            ## Seite: user-guide/configuration.md
            Richtlinie: ...
    """
    guidelines = load_all_guidelines(docs_dir)
    parts: list[str] = []
    for page_path in sorted(guidelines):
        # Use only the first 3 lines of the guideline for compactness
        snippet = guidelines[page_path]
        snippet_lines = snippet.strip().split("\n")
        if len(snippet_lines) > 3:
            snippet = "\n".join(snippet_lines[:3]) + "\n..."
        parts.append(f"## Seite: {page_path}\nRichtlinie: {snippet}")

    result = "\n\n".join(parts)
    if max_chars > 0 and len(result) > max_chars:
        result = result[:max_chars] + "\n\n[... gekürzt ...]"
    return result
