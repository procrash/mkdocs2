"""Build MkDocs navigation structure from generated files."""
from __future__ import annotations
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def build_nav(output_dir: Path) -> list:
    """Build the MkDocs nav structure from the docs directory.

    Scans generated/ and manual/ directories and creates a nav list.
    """
    docs_dir = output_dir / "docs"
    nav: list = []

    # Home
    if (docs_dir / "index.md").exists():
        nav.append({"Home": "index.md"})

    # User / Getting Started
    user_nav = _build_section_nav(docs_dir, "generated/user", "Getting Started")
    if user_nav:
        nav.append({"Getting Started": user_nav})

    # Developer Guide
    dev_nav = _build_section_nav(docs_dir, "generated/developer", "Developer Guide")
    if dev_nav:
        nav.append({"Developer Guide": dev_nav})

    # API Reference
    api_nav = _build_section_nav(docs_dir, "generated/api", "API Reference")
    if api_nav:
        nav.append({"API Reference": api_nav})

    # Manual
    manual_nav = _build_section_nav(docs_dir, "manual", "Manual")
    if manual_nav:
        nav.append({"Manual": manual_nav})

    return nav


def _build_section_nav(docs_dir: Path, section_path: str, section_name: str) -> list:
    """Build navigation for a section directory."""
    section_dir = docs_dir / section_path
    if not section_dir.exists():
        return []

    items: list = []

    # Index first
    index_file = section_dir / "index.md"
    if index_file.exists():
        items.append({"Overview": f"{section_path}/index.md"})

    # Special files (non-directory)
    for md_file in sorted(section_dir.glob("*.md")):
        if md_file.name == "index.md":
            continue
        title = _title_from_filename(md_file.stem)
        items.append({title: f"{section_path}/{md_file.name}"})

    # Subdirectories
    for subdir in sorted(section_dir.iterdir()):
        if not subdir.is_dir():
            continue
        sub_items = []
        sub_index = subdir / "index.md"
        rel_subdir = f"{section_path}/{subdir.name}"

        if sub_index.exists():
            sub_items.append({"Overview": f"{rel_subdir}/index.md"})

        for md_file in sorted(subdir.glob("*.md")):
            if md_file.name == "index.md":
                continue
            title = _title_from_filename(md_file.stem)
            sub_items.append({title: f"{rel_subdir}/{md_file.name}"})

        if sub_items:
            dir_title = _title_from_filename(subdir.name)
            items.append({dir_title: sub_items})

    return items


def _title_from_filename(stem: str) -> str:
    """Convert a filename stem to a readable title."""
    return stem.replace("-", " ").replace("_", " ").title()
