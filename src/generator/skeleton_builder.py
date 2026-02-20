"""Build documentation skeleton with placeholder markdown before generation."""
from __future__ import annotations
import logging
from pathlib import Path

from ..config.schema import AppConfig, SkeletonSuggestionEntry

logger = logging.getLogger(__name__)

# Default skeleton structure: (relative_path, title, body_template)
DEFAULT_SKELETON: list[tuple[str, str, str]] = [
    # Root
    ("index.md", "Projektübersicht", _LANDING_BODY := """
Willkommen zur automatisch generierten Dokumentation für **{project_name}**.

!!! info "Automatische Generierung"
    Diese Dokumentation wird gerade von mkdocsOnSteroids erstellt.
    Seiten werden nach und nach befüllt.

## Dokumentationsabschnitte

| Abschnitt | Beschreibung |
|-----------|-------------|
| [Erste Schritte](getting-started/index.md) | Installation & Schnellstart |
| [Entwickler](generated/developer/index.md) | Technische Dokumentation |
| [API-Referenz](generated/api/index.md) | API-Endpunkte & Schemas |
| [Architektur](architecture/index.md) | System-Architektur & Diagramme |
| [Handbuch](manual/index.md) | Manuell gepflegte Seiten |
"""),

    # Getting started
    ("getting-started/index.md", "Erste Schritte", """
!!! tip "Wird automatisch befüllt"
    Dieser Abschnitt wird durch die Dokumentationsgenerierung ergänzt.

## Inhalte

- [Installation](installation.md)
- [Schnellstart](quickstart.md)
"""),
    ("getting-started/installation.md", "Installation", """
!!! note "Platzhalter"
    Diese Seite wird automatisch mit Installationsanweisungen befüllt.

## Voraussetzungen

*Wird generiert...*

## Installation

*Wird generiert...*
"""),
    ("getting-started/quickstart.md", "Schnellstart", """
!!! note "Platzhalter"
    Diese Seite wird automatisch mit einem Schnellstart-Guide befüllt.

## Erste Schritte

*Wird generiert...*
"""),

    # Generated developer
    ("generated/developer/index.md", "Entwickler-Dokumentation", """
!!! info "Automatisch generiert"
    Technische Dokumentation für Entwickler.

## Abschnitte

- [Klassen](classes/index.md)
- [Module](modules/index.md)
- [Diagramme](diagrams/index.md)
"""),
    ("generated/developer/architecture.md", "Architektur", """
!!! note "Platzhalter"
    Architekturübersicht wird generiert.

```mermaid
graph TD
    A[Quellcode] --> B[Analyse]
    B --> C[Generierung]
    C --> D[Dokumentation]
```
"""),
    ("generated/developer/classes/index.md", "Klassen", """
!!! info "Wird befüllt"
    Hier erscheinen automatisch generierte Klassen-Dokumentationen.
"""),
    ("generated/developer/modules/index.md", "Module", """
!!! info "Wird befüllt"
    Hier erscheinen automatisch generierte Modul-Dokumentationen.
"""),
    ("generated/developer/diagrams/index.md", "Diagramme", """
!!! info "Wird befüllt"
    Hier erscheinen automatisch generierte Diagramme.
"""),

    # Generated API
    ("generated/api/index.md", "API-Referenz", """
!!! info "Automatisch generiert"
    API-Dokumentation für Integratoren.

## Abschnitte

- [Endpunkte](endpoints/index.md)
- [Schemas](schemas/index.md)
- [Beispiele](examples/index.md)
"""),
    ("generated/api/endpoints/index.md", "API-Endpunkte", """
!!! info "Wird befüllt"
    Hier erscheinen automatisch generierte API-Endpunkt-Dokumentationen.
"""),
    ("generated/api/schemas/index.md", "Schemas", """
!!! info "Wird befüllt"
    Hier erscheinen automatisch generierte Schema-Dokumentationen.
"""),
    ("generated/api/examples/index.md", "Beispiele", """
!!! info "Wird befüllt"
    Hier erscheinen automatisch generierte API-Beispiele.
"""),

    # Generated user
    ("generated/user/index.md", "Benutzerhandbuch", """
!!! info "Automatisch generiert"
    Dokumentation für Endbenutzer.

## Abschnitte

- [Features](features/index.md)
- [Tutorials](tutorials/index.md)
"""),
    ("generated/user/features/index.md", "Features", """
!!! info "Wird befüllt"
    Hier erscheinen automatisch generierte Feature-Beschreibungen.
"""),
    ("generated/user/tutorials/index.md", "Tutorials", """
!!! info "Wird befüllt"
    Hier erscheinen automatisch generierte Tutorials.
"""),

    # Architecture
    ("architecture/index.md", "Architektur-Überblick", """
!!! info "Wird befüllt"
    System-Architektur und Design-Entscheidungen.

```mermaid
graph LR
    subgraph System
        A[Eingabe] --> B[Verarbeitung]
        B --> C[Ausgabe]
    end
```
"""),
    ("architecture/diagrams/index.md", "Architektur-Diagramme", """
!!! info "Wird befüllt"
    Detaillierte Mermaid-Diagramme zur Systemarchitektur.
"""),

    # Manual
    ("manual/index.md", "Handbuch", """
Manuell gepflegte Dokumentation.

## Seiten

- [FAQ](faq.md)
- [Changelog](changelog.md)
- [Mitwirken](contributing.md)
"""),
    ("manual/faq.md", "FAQ", """
## Häufig gestellte Fragen

*Noch keine Einträge.*
"""),
    ("manual/changelog.md", "Changelog", """
## Änderungsprotokoll

*Noch keine Einträge.*
"""),
    ("manual/contributing.md", "Mitwirken", """
## Beiträge

*Richtlinien werden noch erstellt.*
"""),
]


def create_skeleton(output_dir: Path, project_name: str = "Documentation") -> list[Path]:
    """Create the documentation skeleton with placeholder pages.

    Returns list of created file paths.
    """
    docs_dir = output_dir / "docs"
    created: list[Path] = []

    for rel_path, title, body_template in DEFAULT_SKELETON:
        file_path = docs_dir / rel_path
        if file_path.exists():
            continue

        file_path.parent.mkdir(parents=True, exist_ok=True)
        body = body_template.format(project_name=project_name) if "{project_name}" in body_template else body_template
        content = f"# {title}\n{body}"
        file_path.write_text(content.strip() + "\n", encoding="utf-8")
        created.append(file_path)

    logger.info("Skeleton created: %d files in %s", len(created), docs_dir)
    return created


def create_suggestion_files(
    output_dir: Path,
    suggestions: list[SkeletonSuggestionEntry],
) -> list[Path]:
    """Create markdown files for accepted LLM skeleton suggestions.

    Only creates files for suggestions where accepted=True.
    Returns list of created file paths.
    """
    docs_dir = output_dir / "docs"
    created: list[Path] = []

    for suggestion in suggestions:
        if not suggestion.accepted:
            continue
        file_path = docs_dir / suggestion.path
        if file_path.exists():
            continue

        file_path.parent.mkdir(parents=True, exist_ok=True)
        content = f"""# {suggestion.title}

!!! note "Wird automatisch befüllt"
    {suggestion.description or 'Dieser Abschnitt wird durch die Dokumentationsgenerierung ergänzt.'}

*Inhalt wird generiert...*
"""
        file_path.write_text(content, encoding="utf-8")
        created.append(file_path)
        logger.info("Created suggestion file: %s", file_path)

    return created


def get_skeleton_tree(output_dir: Path) -> list[tuple[str, int]]:
    """Get the skeleton structure as a tree for display.

    Returns list of (display_line, depth) tuples.
    """
    docs_dir = output_dir / "docs"
    if not docs_dir.exists():
        return []

    tree: list[tuple[str, int]] = []
    _walk_tree(docs_dir, docs_dir, tree, depth=0)
    return tree


def _walk_tree(base: Path, current: Path, tree: list[tuple[str, int]], depth: int) -> None:
    """Recursively walk directory and build tree display."""
    entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name))
    for entry in entries:
        rel = entry.relative_to(base)
        if entry.is_dir():
            tree.append((f"{entry.name}/", depth))
            _walk_tree(base, entry, tree, depth + 1)
        elif entry.suffix == ".md":
            tree.append((entry.name, depth))
