"""Build MkDocs navigation structure from generated files."""
from __future__ import annotations
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Ordered list of top-level sections.
# Each entry: (directory_name, nav_label)
# The order here determines the order in the generated nav.
# "generated/developer" is listed but its content is auto-generated
# so it's scanned dynamically like all other sections.
_SECTION_ORDER: list[tuple[str, str]] = [
    ("getting-started", "Erste Schritte"),
    ("user-guide", "Benutzerhandbuch"),
    ("tutorials", "Tutorials"),
    ("manual", "Bedienungsanleitung"),
    ("formats", "Dateiformate"),
    ("architecture", "Architektur"),
    ("api", "API-Referenz"),
    ("integrations", "Integrationen"),
    ("generated/developer", "Developer Guide"),
    ("development", "Entwicklung"),
    ("operations", "Betrieb"),
    ("compliance", "Compliance"),
    ("reference", "Referenz"),
]


def build_nav(output_dir: Path) -> list:
    """Build the MkDocs nav structure from the docs directory.

    Scans all known section directories in a defined order and creates
    a nav list suitable for mkdocs.yml.
    """
    docs_dir = output_dir / "docs"
    nav: list = []

    if not docs_dir.exists():
        return nav

    # Home
    if (docs_dir / "index.md").exists():
        nav.append({"Home": "index.md"})

    # All sections in defined order
    for section_path, section_label in _SECTION_ORDER:
        section_nav = _build_section_nav(docs_dir, section_path, section_label)
        if section_nav:
            nav.append({section_label: section_nav})

    # Any additional top-level directories not in _SECTION_ORDER
    known_dirs = {s[0].split("/")[0] for s in _SECTION_ORDER}
    known_dirs.add("generated")  # handled via generated/developer etc.
    for subdir in sorted(docs_dir.iterdir()):
        if not subdir.is_dir():
            continue
        if subdir.name in known_dirs or subdir.name.startswith("_") or subdir.name.startswith("."):
            continue
        extra_nav = _build_section_nav(docs_dir, subdir.name, _title_from_filename(subdir.name))
        if extra_nav:
            nav.append({_title_from_filename(subdir.name): extra_nav})

    return nav


def _build_section_nav(docs_dir: Path, section_path: str, section_name: str) -> list:
    """Build navigation for a section directory."""
    section_dir = docs_dir / section_path
    if not section_dir.exists():
        return []

    items: list = []

    # Index first (as "Overview" or section name)
    index_file = section_dir / "index.md"
    if index_file.exists():
        items.append({"Overview": f"{section_path}/index.md"})

    # Top-level .md files in section (non-index)
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
