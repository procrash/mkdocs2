"""Write generated documentation as Markdown files."""
from __future__ import annotations
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


def sanitize_filename(name: str) -> str:
    """Convert a name to a safe filename."""
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")


def write_markdown(
    content: str,
    output_dir: Path,
    stakeholder: str,
    doc_type: str,
    name: str,
) -> Path:
    """Write a markdown file to the appropriate location.

    Structure: output_dir/generated/{stakeholder}/{doc_type}/{name}.md
    """
    # Map doc_types to directory names
    type_dirs = {
        "classes": "classes",
        "modules": "modules",
        "functions": "modules",  # Functions go into modules dir
        "architecture": "",  # Goes directly into developer/
        "diagrams": "diagrams",
        "endpoints": "endpoints",
        "schemas": "schemas",
        "examples": "examples",
        "features": "features",
        "tutorials": "tutorials",
        "getting_started": "",
    }

    subdir = type_dirs.get(doc_type, doc_type)
    safe_name = sanitize_filename(name)

    if subdir:
        file_path = output_dir / "docs" / "generated" / stakeholder / subdir / f"{safe_name}.md"
    else:
        # Special files go directly in stakeholder dir
        special_names = {
            "architecture": "architecture.md",
            "getting_started": "getting-started.md",
        }
        fname = special_names.get(doc_type, f"{safe_name}.md")
        file_path = output_dir / "docs" / "generated" / stakeholder / fname

    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Clean up the content
    cleaned = _clean_markdown(content)

    # Protect skeleton index files: append generated content instead of overwriting
    if file_path.exists() and file_path.name == "index.md":
        logger.info("Skipping index file (skeleton protected): %s", file_path)
        return file_path

    file_path.write_text(cleaned, encoding="utf-8")
    logger.info("Written: %s", file_path)
    return file_path


def _clean_markdown(content: str) -> str:
    """Clean up LLM-generated markdown."""
    # Remove common LLM artifacts
    content = content.strip()

    # Remove wrapping ```markdown ... ``` if present
    if content.startswith("```markdown"):
        content = content[len("```markdown"):].strip()
        if content.endswith("```"):
            content = content[:-3].strip()

    # Ensure single trailing newline
    content = content.rstrip() + "\n"

    return content


def write_manual_placeholder(output_dir: Path, filename: str, title: str) -> Path:
    """Write a placeholder manual page if it doesn't exist."""
    file_path = output_dir / "docs" / "manual" / filename
    if file_path.exists():
        return file_path

    file_path.parent.mkdir(parents=True, exist_ok=True)
    content = f"# {title}\n\n*This page is maintained manually.*\n"
    file_path.write_text(content, encoding="utf-8")
    logger.info("Written manual placeholder: %s", file_path)
    return file_path
