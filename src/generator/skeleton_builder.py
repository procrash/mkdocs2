"""Build documentation skeleton with rich placeholder markdown before generation.

Each skeleton page contains detailed content guidelines describing what
should eventually appear there — useful both as LLM prompt context and
as a human-readable roadmap visible in the early MkDocs preview.
"""
from __future__ import annotations
import logging
from pathlib import Path

from ..config.schema import SkeletonSuggestionEntry

logger = logging.getLogger(__name__)

# Default skeleton structure: (relative_path, title, body_template)
# {project_name} is replaced at creation time.
DEFAULT_SKELETON: list[tuple[str, str, str]] = [
    # ── Root ─────────────────────────────────────────────────────────
    ("index.md", "Projektübersicht", """
Willkommen zur automatisch generierten Dokumentation für **{project_name}**.

!!! info "Automatische Generierung"
    Diese Dokumentation wird von mkdocsOnSteroids erstellt.
    Seiten werden nach und nach mit Inhalten befüllt.

## Dokumentationsabschnitte

| Abschnitt | Beschreibung |
|-----------|-------------|
| [Erste Schritte](getting-started/index.md) | Installation, Konfiguration & Schnellstart |
| [Entwickler](generated/developer/index.md) | Klassen, Module, Architektur, Diagramme |
| [API-Referenz](generated/api/index.md) | Endpunkte, Schemas, Beispiele |
| [Benutzerhandbuch](generated/user/index.md) | Features, Tutorials |
| [Architektur](architecture/index.md) | System-Architektur & Design-Entscheidungen |
| [Handbuch](manual/index.md) | FAQ, Changelog, Mitwirken |
"""),

    # ── Getting Started ──────────────────────────────────────────────
    ("getting-started/index.md", "Erste Schritte", """
!!! tip "Inhaltsrichtlinie"
    Dieser Abschnitt führt neue Benutzer und Entwickler durch die ersten Schritte.

## Inhalte

- [Installation](installation.md) — System aufsetzen
- [Schnellstart](quickstart.md) — In 5 Minuten zum ersten Ergebnis

## Zielgruppe

Dieser Bereich richtet sich an Personen, die das Projekt **zum ersten Mal** verwenden.
Er soll alle nötigen Informationen enthalten, um von Null auf ein funktionierendes Setup zu kommen.
"""),

    ("getting-started/installation.md", "Installation", """
!!! tip "Inhaltsrichtlinie"
    Komplette Schritt-für-Schritt Installationsanleitung.

## Voraussetzungen

Hier sollte stehen:

- **Systemanforderungen**: Betriebssystem, Hardware-Minimum, Festplattenspeicher
- **Software-Abhängigkeiten**: Programmiersprachen, Runtime-Versionen, Paketmanager
- **Netzwerk-Anforderungen**: Ports, Firewall-Regeln, externe Dienste

## Installation

Hier sollte stehen:

1. **Repository klonen** oder Paket herunterladen
2. **Abhängigkeiten installieren** (z.B. `pip install`, `npm install`, `apt-get`)
3. **Konfigurationsdatei erstellen** und anpassen
4. **Installation verifizieren** (Health-Check, Testlauf)

## Nach der Installation

- Erste Konfigurationsschritte
- Verifikation: Wie prüft man, ob alles funktioniert?
- Häufige Probleme bei der Installation und deren Lösungen

## Docker / Container

Falls zutreffend:

- `docker pull` / `docker-compose up` Anleitung
- Umgebungsvariablen und Volumes
- Port-Mapping
"""),

    ("getting-started/quickstart.md", "Schnellstart", """
!!! tip "Inhaltsrichtlinie"
    Minimaler Guide: vom Start zum ersten Ergebnis in wenigen Minuten.

## Schnellstart in 5 Minuten

Hier sollte stehen:

1. **Minimalste Installation** (ein Befehl wenn möglich)
2. **Erstes Beispiel ausführen** (Hello World / Demo)
3. **Ergebnis prüfen** — was sollte man sehen?
4. **Nächste Schritte** — Verweis auf tiefergehende Dokumentation

## Beispiel-Konfiguration

```yaml
# Minimale Konfiguration hier einfügen
```

## Typischer Workflow

Beschreibung des üblichen Arbeitsablaufs mit dem Projekt.
"""),

    # ── Generated: Developer ─────────────────────────────────────────
    ("generated/developer/index.md", "Entwickler-Dokumentation", """
!!! tip "Inhaltsrichtlinie"
    Technische Dokumentation für Entwickler, die am Projekt arbeiten oder es erweitern.

## Abschnitte

- [Klassen](classes/index.md) — Klassenhierarchie und Verantwortlichkeiten
- [Module](modules/index.md) — Modulstruktur und Abhängigkeiten
- [Diagramme](diagrams/index.md) — Visualisierungen der Architektur

## Für Entwickler

Dieser Bereich enthält:

- **Code-Dokumentation**: Auto-generierte Beschreibungen von Klassen, Funktionen, Modulen
- **Architekturentscheidungen**: Warum wurde was wie implementiert?
- **Abhängigkeiten**: Welche Bibliotheken/Frameworks werden genutzt und warum?
- **Code-Konventionen**: Naming, Formatierung, Patterns
"""),

    ("generated/developer/architecture.md", "Architektur", """
!!! tip "Inhaltsrichtlinie"
    Technische Architekturübersicht mit Diagrammen.

## Systemarchitektur

Hier sollte stehen:

- **High-Level-Diagramm** der Hauptkomponenten
- **Datenfluss** zwischen den Komponenten
- **Schnittstellen** zwischen Modulen

```mermaid
graph TD
    A[Eingabe] --> B[Verarbeitung]
    B --> C[Ausgabe]
    B --> D[Persistenz]
```

## Komponentenübersicht

| Komponente | Verantwortlichkeit | Abhängigkeiten |
|-----------|-------------------|----------------|
| *wird generiert* | | |

## Design Patterns

Welche Entwurfsmuster werden verwendet (z.B. Observer, Factory, Strategy)?

## Fehlerbehandlung

Strategie für Error-Handling, Logging, Recovery.
"""),

    ("generated/developer/classes/index.md", "Klassen", """
!!! tip "Inhaltsrichtlinie"
    Auto-generierte Dokumentation aller Klassen im Projekt.

## Erwarteter Inhalt

Für jede Klasse:

- **Klassenname** und Modul-Zugehörigkeit
- **Verantwortlichkeit** (Single Responsibility)
- **Konstruktor-Parameter** und deren Typen
- **Öffentliche Methoden** mit Signatur und Beschreibung
- **Vererbungshierarchie** (extends/implements)
- **Verwendungsbeispiel**
"""),

    ("generated/developer/modules/index.md", "Module", """
!!! tip "Inhaltsrichtlinie"
    Auto-generierte Dokumentation aller Module/Packages im Projekt.

## Erwarteter Inhalt

Für jedes Modul:

- **Modulname** und Pfad
- **Zweck** des Moduls (was macht es, warum existiert es?)
- **Öffentliche Schnittstelle** (exportierte Funktionen, Klassen, Konstanten)
- **Abhängigkeiten** (welche anderen Module werden importiert?)
- **Konfiguration** (falls das Modul konfigurierbar ist)
"""),

    ("generated/developer/diagrams/index.md", "Diagramme", """
!!! tip "Inhaltsrichtlinie"
    Auto-generierte Mermaid-Diagramme zur Visualisierung der Codestruktur.

## Erwarteter Inhalt

- **Klassendiagramme**: Vererbung und Beziehungen
- **Sequenzdiagramme**: Typische Abläufe/Workflows
- **Komponentendiagramme**: Modulstruktur und Abhängigkeiten
- **Zustandsdiagramme**: State Machines (falls vorhanden)

```mermaid
classDiagram
    class Beispiel {
        +methode()
        -attribut: Typ
    }
```
"""),

    # ── Generated: API ───────────────────────────────────────────────
    ("generated/api/index.md", "API-Referenz", """
!!! tip "Inhaltsrichtlinie"
    Vollständige API-Dokumentation für Integratoren und externe Entwickler.

## Abschnitte

- [Endpunkte](endpoints/index.md) — REST/GraphQL Endpunkte
- [Schemas](schemas/index.md) — Datenmodelle und Typen
- [Beispiele](examples/index.md) — Request/Response-Beispiele

## Übersicht

Hier sollte stehen:

- **Base URL** und Versioning-Strategie
- **Authentifizierung** (API-Key, OAuth, Bearer Token)
- **Rate Limiting** und Quotas
- **Fehler-Codes** und deren Bedeutung
"""),

    ("generated/api/endpoints/index.md", "API-Endpunkte", """
!!! tip "Inhaltsrichtlinie"
    Alle API-Endpunkte mit Methode, Pfad, Parametern und Antworten.

## Erwarteter Inhalt

Für jeden Endpunkt:

- **HTTP-Methode** (GET, POST, PUT, DELETE)
- **Pfad** mit Path- und Query-Parametern
- **Request Body** (Schema, Pflichtfelder, Beispiel)
- **Response** (Status-Codes, Body-Schema, Beispiel)
- **Fehler-Antworten** (4xx, 5xx mit Beschreibung)
"""),

    ("generated/api/schemas/index.md", "Schemas", """
!!! tip "Inhaltsrichtlinie"
    Datenmodelle und Typdefinitionen die in der API verwendet werden.

## Erwarteter Inhalt

Für jedes Schema/Model:

- **Name** und Beschreibung
- **Felder** mit Typ, Pflicht/Optional, Default-Wert
- **Validierungsregeln** (min/max, Pattern, Enum-Werte)
- **Beziehungen** zu anderen Schemas
- **JSON-Beispiel**
"""),

    ("generated/api/examples/index.md", "Beispiele", """
!!! tip "Inhaltsrichtlinie"
    Praxisnahe Request/Response-Beispiele für die API.

## Erwarteter Inhalt

- **cURL-Beispiele** für jeden wichtigen Endpunkt
- **Python/JavaScript-Beispiele** mit gängigen HTTP-Bibliotheken
- **Typische Workflows** (z.B. "Benutzer erstellen → Einloggen → Daten abfragen")
- **Fehlerbehandlung** in Client-Code
"""),

    # ── Generated: User ──────────────────────────────────────────────
    ("generated/user/index.md", "Benutzerhandbuch", """
!!! tip "Inhaltsrichtlinie"
    Dokumentation für Endbenutzer, die das Projekt verwenden (nicht entwickeln).

## Abschnitte

- [Features](features/index.md) — Was kann das Projekt?
- [Tutorials](tutorials/index.md) — Schritt-für-Schritt Anleitungen

## Zielgruppe

Endbenutzer, Administratoren, Product Owner — alle, die das Projekt **benutzen**
ohne den Quellcode zu verändern.
"""),

    ("generated/user/features/index.md", "Features", """
!!! tip "Inhaltsrichtlinie"
    Übersicht aller Features und Funktionen für Endbenutzer.

## Erwarteter Inhalt

Für jedes Feature:

- **Feature-Name** und Kurzbeschreibung
- **Anwendungsfall**: Wann und warum nutzt man es?
- **Bedienung**: Screenshots, Schritte, Konfigurationsoptionen
- **Einschränkungen**: Was geht nicht, was ist zu beachten?
- **Tipps & Tricks**: Best Practices
"""),

    ("generated/user/tutorials/index.md", "Tutorials", """
!!! tip "Inhaltsrichtlinie"
    Schritt-für-Schritt Anleitungen für häufige Aufgaben.

## Erwarteter Inhalt

Jedes Tutorial sollte:

- Ein **konkretes Ziel** haben (z.B. "Ersten Report erstellen")
- **Voraussetzungen** nennen
- **Nummerierte Schritte** mit Screenshots/Code-Beispielen enthalten
- Mit einem **Ergebnis** enden (was sollte man am Ende sehen?)
- **Troubleshooting** für häufige Fehler enthalten
"""),

    # ── Architecture ─────────────────────────────────────────────────
    ("architecture/index.md", "Architektur-Überblick", """
!!! tip "Inhaltsrichtlinie"
    Gesamtarchitektur des Systems mit Diagrammen und Designentscheidungen.

## Systemübersicht

Hier sollte stehen:

- **High-Level-Architekturdiagramm** (Mermaid)
- **Hauptkomponenten** und ihre Verantwortlichkeiten
- **Datenfluss** zwischen Komponenten

```mermaid
graph LR
    subgraph System
        A[Eingabe] --> B[Verarbeitung]
        B --> C[Ausgabe]
    end
```

## Technologie-Stack

- Verwendete Frameworks, Bibliotheken, Datenbanken
- Begründung der Technologieentscheidungen

## Design-Entscheidungen

- Architekturmuster (MVC, Microservices, Event-driven, etc.)
- Trade-offs und Begründungen

## Deployment

- Deployment-Architektur (Server, Container, Cloud)
- Skalierungsstrategie
- Monitoring und Observability
"""),

    ("architecture/diagrams/index.md", "Architektur-Diagramme", """
!!! tip "Inhaltsrichtlinie"
    Detaillierte Mermaid-Diagramme zur Systemarchitektur.

## Erwarteter Inhalt

- **Komponentendiagramm**: Welche Teile gibt es und wie hängen sie zusammen?
- **Sequenzdiagramm**: Ablauf typischer Requests/Workflows
- **Deployment-Diagramm**: Wo läuft was (Server, Container, Services)?
- **ER-Diagramm**: Datenbank-Schema (falls zutreffend)

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Database
    Client->>Server: Request
    Server->>Database: Query
    Database-->>Server: Result
    Server-->>Client: Response
```
"""),

    # ── Manual ───────────────────────────────────────────────────────
    ("manual/index.md", "Handbuch", """
Manuell gepflegte Dokumentation, die nicht automatisch generiert wird.

## Seiten

- [FAQ](faq.md) — Häufig gestellte Fragen
- [Changelog](changelog.md) — Versionshistorie
- [Mitwirken](contributing.md) — Beitragsrichtlinien
"""),

    ("manual/faq.md", "FAQ", """
!!! tip "Inhaltsrichtlinie"
    Häufig gestellte Fragen und Antworten.

## Erwarteter Inhalt

Typische Fragen zu:

- **Installation**: "Es funktioniert nicht, was tun?"
- **Konfiguration**: "Wie ändere ich X?"
- **Betrieb**: "Warum ist Y langsam?"
- **Fehlerbehebung**: "Fehlercode Z — was bedeutet das?"

Jede Frage sollte eine **klare, kurze Antwort** und ggf. einen Link zur ausführlichen Dokumentation enthalten.
"""),

    ("manual/changelog.md", "Changelog", """
!!! tip "Inhaltsrichtlinie"
    Versionshistorie nach [Keep a Changelog](https://keepachangelog.com/) Format.

## Format

```markdown
## [1.0.0] - 2024-01-01
### Added
- Neue Funktion X

### Changed
- Verhalten von Y geändert

### Fixed
- Bug in Z behoben

### Removed
- Veraltete Funktion W entfernt
```
"""),

    ("manual/contributing.md", "Mitwirken", """
!!! tip "Inhaltsrichtlinie"
    Richtlinien für Beiträge zum Projekt.

## Erwarteter Inhalt

- **Wie kann ich beitragen?** (Issues, Pull Requests, Discussions)
- **Entwicklungsumgebung einrichten** (Fork, Clone, Branch-Strategie)
- **Code-Konventionen** (Style Guide, Linting, Formatierung)
- **Tests schreiben** (Framework, Coverage-Anforderungen)
- **Commit-Messages** (Format, Konventionen)
- **Review-Prozess** (Wer reviewed? Wie lange dauert es?)
- **Code of Conduct** (Verhaltensrichtlinien)
"""),
]


def create_skeleton(output_dir: Path, project_name: str = "Documentation") -> list[Path]:
    """Create the documentation skeleton with rich placeholder pages.

    Returns list of created file paths.  Existing files are never overwritten.
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

!!! tip "Inhaltsrichtlinie"
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
        if entry.is_dir():
            tree.append((f"{entry.name}/", depth))
            _walk_tree(base, entry, tree, depth + 1)
        elif entry.suffix == ".md":
            tree.append((entry.name, depth))
